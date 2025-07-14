import secrets
from functools import wraps
from flask import session, flash, redirect, url_for, request, jsonify
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
