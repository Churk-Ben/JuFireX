import secrets
import os
import requests
import uuid
import shutil
from urllib.parse import urlparse, unquote
from functools import wraps
from flask import session, flash, redirect, url_for, request, jsonify, current_app
from .models import db, User, Project, NavItem
from .config import ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_MEMBER


# 权限检查装饰器
def require_role(min_role, owner_check=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("请先登录", "warning")
                return redirect(url_for("auth.login"))

            user = db.session.get(User, session["user_id"])
            if not user or not user.is_active:
                flash("用户不存在或已被禁用", "error")
                return redirect(url_for("auth.login"))

            # 基本角色检查
            if user.role < min_role:
                flash("权限不足", "error")
                return redirect(url_for("index"))

            # 可选的所有权或更复杂的检查
            if owner_check:
                if not owner_check(user, **kwargs):
                    flash("权限不足或操作不允许", "error")
                    # 对于API端点，返回JSON错误可能更合适
                    if request.path.startswith("/api/"):
                        return (
                            jsonify(
                                {"success": False, "message": "权限不足或操作不允许"}
                            ),
                            403,
                        )
                    return redirect(url_for("index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# 所有权检查函数
def is_project_owner_or_admin(user, project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 超级管理员或管理员可以管理
    if user.role >= ROLE_ADMIN:
        return True
    # 作者可以管理自己的项目
    return project.author_id == user.id


def can_manage_project(user, project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 超级管理员可以管理所有项目
    if user.role == ROLE_SUPER_ADMIN:
        return True
    # 管理员可以管理非超级管理员和非管理员创建的项目
    if user.role == ROLE_ADMIN:
        return project.author.role < ROLE_ADMIN
    # 成员只能管理自己的项目
    if user.role == ROLE_MEMBER:
        return project.author_id == user.id
    return False


def can_manage_nav_item(user, item_id):
    item = db.session.get(NavItem, item_id)
    if not item:
        return False
    if user.role == ROLE_SUPER_ADMIN:
        return True
    if user.role == ROLE_ADMIN:
        return item.creator.role < ROLE_ADMIN
    return item.created_by == user.id


def can_manage_user(user, user_id):
    # 只有超级管理员可以管理用户
    return user.role == ROLE_SUPER_ADMIN


# CSRF保护函数
def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)
    return session["_csrf_token"]


def validate_csrf_token():
    csrf_token = request.headers.get("X-CSRFToken")
    return csrf_token and csrf_token == session.get("_csrf_token")


def delete_cached_image(image_url):
    if not image_url or not image_url.startswith('/cache/'):
        return

    try:
        filename = os.path.basename(image_url)
        # 尝试从两个可能的缓存目录中删除
        for folder in ['using_cache', 'user_data']:
            file_path = os.path.join(current_app.root_path, folder, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"Deleted cached image: {file_path}")
                return
    except Exception as e:
        current_app.logger.error(f"Error deleting cached image {image_url}: {e}")


def cache_image_from_url(image_url, storage_folder='using_cache'):
    if not image_url:
        return None

    try:
        # 检查是否已经是本地缓存的URL
        if image_url.startswith('/cache/'):
            return image_url

        result = urlparse(image_url)

        # 处理本地文件 URI (file://...)
        if result.scheme == 'file':
            # unquote to handle spaces and special characters in file path
            local_path = unquote(result.path)
            # On Windows, file:// URI path might start with a slash, e.g., /C:/Users/...
            if os.name == 'nt' and local_path.startswith('/'):
                local_path = local_path[1:]

            if not os.path.exists(local_path):
                current_app.logger.error(f"Local file not found: {local_path}")
                return None

            ext = os.path.splitext(local_path)[1]
            if not ext:
                current_app.logger.error(f"Cannot determine file type from path: {local_path}")
                return None  # 无法确定文件类型

            filename = f"{uuid.uuid4().hex}{ext}"
            cache_dir = os.path.join(current_app.root_path, storage_folder)
            os.makedirs(cache_dir, exist_ok=True)
            new_file_path = os.path.join(cache_dir, filename)

            shutil.copy(local_path, new_file_path)
            current_app.logger.info(f"Copied local file from {local_path} to {new_file_path}")

            return f"/cache/{filename}"

        # 处理网络 URL
        if not all([result.scheme, result.netloc]):
            return image_url  # 不是有效的URL，可能已经是本地路径

        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()

        # 获取文件扩展名
        content_type = response.headers.get('Content-Type')
        if content_type and 'image' in content_type:
            ext = '.' + content_type.split('/')[1].split(';')[0]
        else:
            path = urlparse(image_url).path
            ext = os.path.splitext(path)[1]
            if not ext:
                return None

        filename = f"{uuid.uuid4().hex}{ext}"
        cache_dir = os.path.join(current_app.root_path, storage_folder)
        os.makedirs(cache_dir, exist_ok=True)
        file_path = os.path.join(cache_dir, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return f"/cache/{filename}"

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to download image from {image_url}: {e}")
        return None
    except FileNotFoundError as e:
        current_app.logger.error(f"File operation error: {e}")
        return None
    except Exception as e:
        current_app.logger.error(f"An error occurred while caching image: {e}")
        return None
