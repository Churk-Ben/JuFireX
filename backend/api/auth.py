from flask import Blueprint, jsonify, request, session

from backend.config import ROLE_GUEST
from backend.core.Security import require_login
from backend.data.models.user import User
from backend.data import users  # Unified Data Access

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"level": "warning", "message": "缺少用户名或密码"}), 400

    user = users.get_by_username(username)
    if user and user.check_password(password) and user.is_active:
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        return jsonify(
            {"level": "success", "message": "登录成功", "user": user.to_dict()}
        )

    return jsonify({"level": "warning", "message": "无效的用户名或密码"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """注销当前登录用户"""
    session.clear()
    return (
        jsonify({"level": "success", "message": "注销成功"}),
        200,
    )


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"level": "warning", "message": "缺少用户名、邮箱或密码"}), 400

    if users.get_by_username(username):
        return jsonify({"level": "warning", "message": "用户名已存在"}), 409

    if users.get_by_email(email):
        return jsonify({"level": "warning", "message": "邮箱已注册"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    # First user becomes Super Admin (Optional logic, can be kept)
    if users.count() == 0:
        from ..config import ROLE_SUPER_ADMIN

        user.role = ROLE_SUPER_ADMIN
    else:
        user.role = ROLE_GUEST  # Default role

    users.create(user)
    return (
        jsonify({"level": "success", "message": "注册成功", "user": user.to_dict()}),
        201,
    )


@auth_bp.route("/me", methods=["GET"])
@require_login
def get_current_user():
    """获取当前登录用户的信息"""
    user_id = session.get("user_id")
    user = users.get(user_id)
    if not user:
        return jsonify({"level": "warning", "message": "用户不存在"}), 404
    return jsonify(
        {"level": "success", "message": "获取用户成功", "user": user.to_dict()}
    )
