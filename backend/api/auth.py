# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 认证模块, 包含登录, 注册, 注销
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, session

from backend.core.Logger import get_logger
from backend.core.Security import require_login
from backend.services import user_service, verification_service


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


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    @name: 用户注册
    @expect:
    {
        "username": "user",
        "email": "user@example.com",
        "password": "123456",
        "code": "123456"
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
    code = data.get("code")

    if not all([username, email, password, code]):
        logger.debug("注册请求缺少用户名/邮箱/密码/验证码")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "请填写完整注册信息",
                }
            ),
            400,
        )

    success, message, user = user_service.register(username, email, password, code)

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


@auth_bp.route("/code/send", methods=["POST"])
def send_code():
    """
    @name: 发送验证码 (通用)
    @expect:
    {
        "identifier": "user@example.com",
        "method": "email",
        "scene": "register"
    }
    @return:
    {
        "level": "success",
        "message": "验证码发送成功",
    }
    """
    data: dict = request.get_json()
    identifier = data.get("identifier")
    method = data.get("method", "email")
    scene = data.get("scene", "register")

    if not identifier:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "请输入邮箱",
                },
            ),
            400,
        )

    if scene == "register" and method == "email":
        if user_service.is_email_registered(identifier):
            return (
                jsonify(
                    {
                        "level": "warning",
                        "message": "该邮箱已被注册",
                    }
                ),
                400,
            )

    success, message = verification_service.send_code(identifier, method, scene)

    if success:
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            400,
        )


@auth_bp.route("/code/verify", methods=["POST"])
def verify_code():
    """
    @name: 验证验证码 (通用，不消耗)
    @expect:
    {
        "identifier": "user@example.com",
        "code": "123456",
        "method": "email",
        "scene": "register"
    }
    @return:
    {
        "level": "success",
        "message": "验证成功",
    }
    """
    data: dict = request.get_json()
    identifier = data.get("identifier")
    code = data.get("code")
    method = data.get("method", "email")
    scene = data.get("scene", "register")

    if not all([identifier, code]):
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "请输入完整验证信息",
                },
            ),
            400,
        )

    success, message = verification_service.verify_code(identifier, code, method, scene)

    if success:
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            400,
        )


@auth_bp.route("/2fa/setup", methods=["GET"])
@require_login
def setup_2fa():
    """
    @name: 生成 TOTP 链接 (设置 2FA)
    @expect: None
    @return:
    {
        "level": "success",
        "message": "生成 TOTP 链接成功",
        "data": {
            "uri": "otpauth://totp/...",
        }
    }
    """
    # TODO: 实现 TOTP 生成逻辑
    return (
        jsonify(
            {
                "level": "info",
                "message": "功能开发中",
            },
        ),
        200,
    )


@auth_bp.route("/2fa/enable", methods=["POST"])
@require_login
def enable_2fa():
    """
    @name: 验证并启用 2FA
    @expect:
    {
        "code": "123456",
    }
    @return:
    {
        "level": "success",
        "message": "2FA 已启用",
    }
    """
    # TODO: 实现 TOTP 验证并绑定逻辑
    return (
        jsonify(
            {
                "level": "info",
                "message": "功能开发中",
            },
        ),
        200,
    )


@auth_bp.route("/2fa/verify", methods=["POST"])
def verify_2fa():
    """
    @name: 登录二次验证
    @expect:
    {
        "uuid": "user_uuid",
        "code": "123456"
    }
    @return:
    {
        "level": "success",
        "message": "登录成功",
    }
    """
    return (
        jsonify(
            {
                "level": "info",
                "message": "功能开发中",
            },
        ),
        200,
    )
