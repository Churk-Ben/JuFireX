# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 用户相关 API (头像上传, 个人信息等)
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, send_from_directory

from backend.config import Config
from backend.core.Logger import get_logger
from backend.core.Security import require_login
from backend.services import user_service

logger = get_logger("API_User")
user_bp = Blueprint("user", __name__)


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

    user = user_service.get_current_user()
    if not user:
        logger.debug("上传请求用户未找到")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "用户未找到",
                }
            ),
            404,
        )

    # 直接传递 FileStorage 对象给 Service
    success, message, filename = user_service.update_avatar(user.id, file)

    if success:
        # 构造头像 URL
        avatar_url = f"/api/user/avatar/{user.uuid}/{filename}"
        logger.debug(f"用户 {user.username} 更新头像成功: {filename}")
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
        logger.warning(f"用户 {user.username} 更新头像失败: {message}")
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
    user_dir = Config.PROFILES_DIR / uuid

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

    if not (user_dir / filename).exists():
        return send_from_directory(Config.DEFAULTS_DIR, filename)
    else:
        return send_from_directory(user_dir, filename)
