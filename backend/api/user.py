# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 用户相关 API (头像上传, 个人信息等)
# ------------------------------------------------------------

from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory, session

from backend.config import Config
from backend.core.Logger import get_logger
from backend.core.Security import (
    require_login,
    require_self_or_super_admin,
    require_super_admin,
)
from backend.services import user_service

logger = get_logger("API_User")
user_bp = Blueprint("user", __name__)


@user_bp.route("/list", methods=["GET"])
@require_super_admin
def list_users():
    """
    @name: 获取所有用户列表
    """

    users = user_service.get_all_users()
    user_list = []
    for u in users:
        user_list.append(
            {
                "uuid": u.uuid,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "role_name": u.get_role_name(),
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
        )

    return jsonify(
        {"level": "success", "message": "获取用户列表成功", "data": user_list}
    )


@user_bp.route("/avatar", methods=["POST"])
@require_login
def upload_avatar():
    """
    @name: 上传并更新用户头像
    @expect:
    {
        "avatar": "file"
    }
    @return:
    {
        "level": "success",
        "message": "头像上传成功",
        "data": {
            "avatar_url": "/api/user/avatar/12345678-1234-5678-1234-567812345678/avatar.jpg",
            "filename": "avatar.jpg",
        }
    }
    """
    if "avatar" not in request.files:
        logger.debug("上传请求缺失头像文件")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "你上传的头像似乎被弄丢了!",
                }
            ),
            400,
        )

    file = request.files["avatar"]
    if file.filename == "":
        logger.debug("上传请求未选择文件")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "未选择文件",
                }
            ),
            400,
        )

    user_uuid = session.get("user_uuid")
    if not user_uuid:
        # 理论上 @require_login 已经保证了有 session, 但为了安全起见
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "用户未登录",
                }
            ),
            401,
        )

    # 直接传递 FileStorage 对象给 Service
    success, message, filename = user_service.update_avatar(user_uuid, file)

    if success:
        # 构造头像 URL
        avatar_url = f"/api/user/avatar/{user_uuid}/{filename}"
        logger.debug(f"用户 {user_uuid} 更新头像成功: {filename}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": {"avatar_url": avatar_url, "filename": filename},
                }
            ),
            200,
        )
    else:
        logger.warning(f"用户 {user_uuid} 更新头像失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            500,
        )


@user_bp.route("/avatar/<uuid>/<filename>")
def get_avatar(uuid, filename):
    """
    @name: 获取用户头像文件
    @expect: None
    @return: 头像文件(file)
    """
    # 头像存储路径: database/profiles/<uuid>/<filename>
    user_dir: Path = Config.PROFILES_DIR / uuid
    avatar_path: Path = user_dir / filename

    if not user_dir.exists():
        logger.debug(f"用户目录不存在: {user_dir}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "用户目录不存在",
                }
            ),
            404,
        )

    if not avatar_path.exists():
        return send_from_directory(Config.DEFAULTS_DIR, filename)
    else:
        return send_from_directory(user_dir, filename)


@user_bp.route("/rebuild/<uuid>", methods=["POST"])
@require_self_or_super_admin
def rebuild_user_dir(uuid):
    """
    @name: 重建用户目录
    @expect:
    {
        "uuid": "用户 UUID (必须与 URL 参数一致)"
    }
    @return:
    {
        "level": "success",
        "message": "用户目录重建成功",
    }
    """
    data: dict = request.get_json()
    body_uuid = data.get("uuid")

    if not body_uuid:
        logger.debug("重建请求缺失用户 UUID")
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "缺少用户 UUID",
                }
            ),
            400,
        )

    # 双重一致性检查: 防止误操作
    if uuid != body_uuid:
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "操作被拒绝: 请求构造不一致",
                }
            ),
            403,
        )

    success, message = user_service.rebuild(uuid)
    if success:
        logger.debug(f"用户目录 {uuid} 重建成功")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                },
            ),
            200,
        )
    else:
        logger.warning(f"用户目录 {uuid} 重建失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                }
            ),
            500,
        )
