import secrets
import os
import requests
import uuid
import shutil
from datetime import datetime
from urllib.parse import urlparse, unquote
from functools import wraps
from flask import session, flash, redirect, url_for, request, jsonify, current_app
from .models import (
    db,
    StudioInfo,
    User,
    Project,
    NavCategory,
    NavItem,
    HiddenNavItem,
)
from .config import (
    ROLE_GUEST,
    ROLE_MEMBER,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
    ROLE_NAMES,
)


# 检查装饰器
def require_role(min_role, owner_check=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查用户是否已登录
            if "user_id" not in session:
                flash("请先登录", "warning")
                return redirect(url_for("auth.login"))

            user = db.session.get(User, session["user_id"])
            if not user or not user.is_active:
                flash("用户不存在或已被封禁", "error")
                return redirect(url_for("auth.login"))

            # 权限检查: 用户达到权限或拥有操作所有权则通过
            has_role_permission = user.role >= min_role
            has_ownership = owner_check and owner_check(user, **kwargs)

            # 如果用户权限不足且没有所有权，则拒绝访问
            if not has_role_permission and not has_ownership:
                # TODO: 重定向到403
                flash("权限不足或操作不允许", "error")
                if request.path.startswith("/api/"):
                    return (
                        jsonify({"success": False, "message": "权限不足或操作不允许"}),
                        403,
                    )
                else:
                    return redirect(url_for("index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# 所有权检查函数
def is_project_owner_or_admin(user, project_id):
    """检查用户是否为项目所有者"""
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 检查是否为项目作者
    return project.author_id == user.id


def can_manage_project(user, project_id):
    """检查用户是否可以管理项目"""
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 只检查是否为项目作者
    return project.author_id == user.id


def can_manage_nav_item(user, item_id):
    """检查用户是否可以管理导航项"""
    item = db.session.get(NavItem, item_id)
    if not item:
        return False
    # 只检查是否为创建者
    return item.created_by == user.id


def can_manage_user(user, user_id):
    """检查用户是否可以管理其他用户"""
    # 用户只能管理自己
    return user.id == user_id


# CSRF保护函数
def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)
    return session["_csrf_token"]


def validate_csrf_token():
    csrf_token = request.headers.get("X-CSRFToken")
    return csrf_token and csrf_token == session.get("_csrf_token")


# 项目数据文件 TODO: 更改服务层位置
def delete_user_data_file(file_url):
    """删除用户数据文件"""
    if not file_url or not file_url.startswith("/user_data/"):
        return

    try:
        filename = os.path.basename(file_url)
        file_path = os.path.join(current_app.root_path, "user_data", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            current_app.logger.info(f"Deleted user data file: {file_path}")
    except Exception as e:
        current_app.logger.error(f"Error deleting user data file {file_url}: {e}")


def save_file_to_user_data(file_url, storage_folder="user_data"):
    """将文件保存到用户数据目录"""
    if not file_url:
        return None

    try:
        # 检查是否已经是本地用户数据URL
        if file_url.startswith("/user_data/"):
            return file_url

        result = urlparse(file_url)

        # 处理本地文件 URI (file://...)
        if result.scheme == "file":
            # unquote to handle spaces and special characters in file path
            local_path = unquote(result.path)
            # On Windows, file:// URI path might start with a slash, e.g., /C:/Users/...
            if os.name == "nt" and local_path.startswith("/"):
                local_path = local_path[1:]

            if not os.path.exists(local_path):
                current_app.logger.error(f"Local file not found: {local_path}")
                return None

            ext = os.path.splitext(local_path)[1]
            if not ext:
                current_app.logger.error(
                    f"Cannot determine file type from path: {local_path}"
                )
                return None  # 无法确定文件类型

            filename = f"{uuid.uuid4().hex}{ext}"
            user_data_dir = os.path.join(current_app.root_path, storage_folder)
            os.makedirs(user_data_dir, exist_ok=True)
            new_file_path = os.path.join(user_data_dir, filename)

            shutil.copy(local_path, new_file_path)
            current_app.logger.info(
                f"Copied local file from {local_path} to {new_file_path}"
            )

            return f"/user_data/{filename}"

        # 处理网络 URL
        if not all([result.scheme, result.netloc]):
            return file_url  # 不是有效的URL，可能已经是本地路径

        response = requests.get(file_url, stream=True, timeout=10)
        response.raise_for_status()

        # 获取文件扩展名
        content_type = response.headers.get("Content-Type")
        if content_type and "image" in content_type:
            ext = "." + content_type.split("/")[1].split(";")[0]
        else:
            path = urlparse(file_url).path
            ext = os.path.splitext(path)[1]
            if not ext:
                return None

        filename = f"{uuid.uuid4().hex}{ext}"
        user_data_dir = os.path.join(current_app.root_path, storage_folder)
        os.makedirs(user_data_dir, exist_ok=True)
        file_path = os.path.join(user_data_dir, filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return f"/user_data/{filename}"

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to download file from {file_url}: {e}")
        return None
    except FileNotFoundError as e:
        current_app.logger.error(f"File operation error: {e}")
        return None
    except Exception as e:
        current_app.logger.error(f"An error occurred while saving file: {e}")
        return None


def get_project_folder_name(project_id, created_at):
    """生成项目文件夹名称 - 多级目录结构"""
    year = created_at.strftime("%Y")
    month = created_at.strftime("%m")
    day = created_at.strftime("%d")
    return os.path.join(year, month, day, str(project_id))


def create_project_folder(project_id, created_at):
    """创建项目文件夹"""
    folder_name = get_project_folder_name(project_id, created_at)
    project_path = os.path.join(current_app.config["PROJECTS_FOLDER"], folder_name)

    try:
        os.makedirs(project_path, exist_ok=True)
        return project_path, folder_name
    except Exception as e:
        current_app.logger.error(f"Failed to create project folder: {e}")
        return None, None


def get_project_folder_path(project_id, created_at):
    """获取项目文件夹路径"""
    folder_name = get_project_folder_name(project_id, created_at)
    return os.path.join(current_app.config["PROJECTS_FOLDER"], folder_name)


def save_project_metadata(project_path, project_data):
    """保存项目元数据到JSON文件"""
    import json

    metadata_path = os.path.join(project_path, "project.json")

    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to save project metadata: {e}")
        return False


def load_project_metadata(project_path):
    """从JSON文件加载项目元数据"""
    import json

    metadata_path = os.path.join(project_path, "project.json")

    try:
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    except Exception as e:
        current_app.logger.error(f"Failed to load project metadata: {e}")
        return None


def delete_project_folder(project_id, created_at):
    """删除项目文件夹"""
    project_path = get_project_folder_path(project_id, created_at)

    try:
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to delete project folder: {e}")
        return False


def get_project_files(project_path, include_hidden=False):
    """获取项目文件夹中的所有文件"""
    files = []

    try:
        if not os.path.exists(project_path):
            return files

        for item in os.listdir(project_path):
            if not include_hidden and item.startswith("."):
                continue

            item_path = os.path.join(project_path, item)
            if os.path.isfile(item_path):
                stat = os.stat(item_path)
                is_markdown = item.lower().endswith((".md", ".markdown"))
                files.append(
                    {
                        "name": item,
                        "path": item,
                        "size": stat.st_size,
                        "modified_time": datetime.fromtimestamp(stat.st_mtime),
                        "is_markdown": is_markdown,
                        "type": "file",
                    }
                )
            elif os.path.isdir(item_path):
                files.append({"name": item, "path": item, "type": "directory"})

        # 按类型和名称排序: 目录在前，文件在后，同类型按名称排序
        files.sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
        return files

    except Exception as e:
        current_app.logger.error(f"Failed to get project files: {e}")
        return files
