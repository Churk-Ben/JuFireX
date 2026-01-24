# ------------------------------------------------------------
# @author: Churk
# @description: 用户相关 API (头像上传, 个人信息等)
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, send_from_directory, current_app
from backend.core.Security import require_login
from backend.core.Logger import get_logger
from backend.services import user_service
from backend.config import Config
import os

logger = get_logger("API_User")
user_bp = Blueprint("user", __name__)


@user_bp.route("/avatar", methods=["POST"])
@require_login
def upload_avatar():
    """上传并更新用户头像"""
    if 'avatar' not in request.files:
        return jsonify({"level": "warning", "message": "未找到上传的文件"}), 400
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"level": "warning", "message": "未选择文件"}), 400

    user = user_service.get_current_user()
    if not user:
         return jsonify({"level": "error", "message": "用户未找到"}), 404

    # 直接传递 FileStorage 对象给 Service
    success, message, filename = user_service.update_avatar(user.id, file)
    
    if success:
        # 构造头像 URL
        avatar_url = f"/api/user/avatar/{user.uuid}/{filename}"
        logger.info(f"用户 {user.username} 更新头像成功: {filename}")
        return jsonify({
            "level": "success", 
            "message": message, 
            "data": {
                "avatar_url": avatar_url,
                "filename": filename
            }
        })
    else:
        logger.error(f"用户 {user.username} 更新头像失败: {message}")
        return jsonify({"level": "error", "message": message}), 500


@user_bp.route("/avatar/<uuid>/<filename>")
def get_avatar(uuid, filename):
    """获取用户头像文件"""
    # 头像存储路径: database/profiles/<uuid>/<filename>
    # Config.PROFILES_DB_PATH 是 database/profiles/users.db
    # 所以 base_dir 是 database/profiles
    profiles_dir = Config.PROFILES_DB_PATH.parent
    user_dir = profiles_dir / uuid
    
    if not user_dir.exists():
        return jsonify({"level": "error", "message": "用户目录不存在"}), 404
        
    return send_from_directory(user_dir, filename)
