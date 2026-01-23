# ------------------------------------------------------------
# @author: Churk
# @description: 认证模块, 包含登录, 注册, 注销
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request

from backend.core.Security import require_login
from backend.core.Logger import get_logger
from backend.services import user_service


logger = get_logger("API_Auth")
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    data = request.get_json()
    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        logger.debug("登录请求缺少邮箱/UUID或密码")
        return jsonify({"level": "warning", "message": "请输入邮箱/UUID和密码"}), 400

    success, message, user = user_service.login(identifier, password)

    if success:
        logger.info(f"用户 {user.username} 登录成功, uuid: {user.uuid}")
        return jsonify({"level": "success", "message": message, "data": user.to_dict()})
    else:
        logger.debug(f"用户 {identifier} 登录失败：{message}")
        return jsonify({"level": "warning", "message": message}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """注销当前登录用户"""
    user_service.logout()
    logger.info("用户注销成功")
    return jsonify({"level": "success", "message": "注销成功"})


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        logger.debug("注册请求缺少用户名/邮箱/密码")
        return jsonify({"level": "warning", "message": "请填写完整注册信息"}), 400

    success, message, new_user = user_service.register(username, email, password)

    if success:
        logger.info(f"用户 {username} 注册成功, uuid: {new_user.uuid}")
        return jsonify(
            {"level": "success", "message": message, "data": new_user.to_dict()}
        )
    else:
        logger.debug(f"用户 {username} 注册失败：{message}")
        return jsonify({"level": "warning", "message": message}), 400


@auth_bp.route("/me", methods=["GET"])
@require_login
def get_current_user():
    """获取当前登录用户的信息"""
    user = user_service.get_current_user()
    if not user:
        logger.debug("获取当前用户失败：用户未找到")
        return jsonify({"level": "error", "message": "用户未找到"}), 404

    logger.info(f"当前用户 {user.username} 信息：{user.to_dict()}")
    return jsonify({"level": "success", "data": user.to_dict()})
