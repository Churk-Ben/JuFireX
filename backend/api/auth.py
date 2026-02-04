# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 认证模块, 包含登录, 注册, 注销
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, session

from backend.core.Logger import get_logger
from backend.core.Security import require_login
from backend.services import user_service


logger = get_logger("API_Auth")
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    @name: 用户登录
    @expect:
    {
        "identifier": "user@example.com",
        "password": "123456"
    }
    @return:
    {
        "level": "success",
        "message": "登录成功",
        "data": user_obj
    }
    """
    data: dict = request.get_json()
    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        logger.debug("登录请求缺少邮箱/UUID或密码")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "请输入邮箱/ID/uuid和密码",
                }
            ),
            400,
        )

    success, message, user = user_service.login(identifier, password)

    if success:
        # 登录成功, 设置 Session (API 层负责)
        session["user_id"] = user.id
        session["user_uuid"] = user.uuid
        session["role"] = user.role
        session.permanent = True

        logger.info(f"用户 {user.username} 登录成功, uuid: {user.uuid}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": user.to_dict(),
                }
            ),
            200,
        )
    else:
        logger.debug(f"用户 {identifier} 登录失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            401,
        )


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    @name: 用户注册
    @expect:
    {
        "username": "user",
        "email": "user@example.com",
        "password": "123456"
    }
    @return:
    {
        "level": "success",
        "message": "注册成功",
        "data": user_obj,
    }
    """
    data: dict = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        logger.debug("注册请求缺少用户名/邮箱/密码")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "请填写完整注册信息",
                }
            ),
            400,
        )

    success, message, user = user_service.register(username, email, password)

    if success:
        logger.info(f"用户 {user.username} 注册成功, uuid: {user.uuid}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": user.to_dict(),
                }
            ),
            201,
        )
    else:
        logger.debug(f"用户 {user.username} 注册失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            400,
        )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    @name: 注销当前登录用户
    @expect: None
    @return:
    {
        "level": "success",
        "message": "白白~",
    }
    """
    # 获取当前用户信息仅用于日志
    user_uuid = session.get("user_uuid")
    if user_uuid:
        logger.info(f"用户 {user_uuid} 注销成功")
    else:
        logger.info("匿名用户注销")

    session.clear()

    return (
        jsonify(
            {
                "level": "success",
                "message": "白白~",
            }
        ),
        200,
    )


@auth_bp.route("/me", methods=["GET"])
@require_login
def get_current_user():
    """
    @name: 获取当前登录用户的信息
    @expect: None
    @return:
    {
        "level": "success",
        "message": "获取用户信息成功",
        "data": user_obj,
    }
    """
    user_uuid = session.get("user_uuid")
    user = user_service.get_profile(user_uuid)

    if not user:
        logger.debug("获取当前用户失败: 用户未找到")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "用户未找到",
                }
            ),
            404,
        )

    logger.debug(f"当前用户 {user.username} 信息: {user.to_dict()}")
    return (
        jsonify(
            {
                "level": "success",
                "message": "获取用户信息成功",
                "data": user.to_dict(),
            }
        ),
        200,
    )
