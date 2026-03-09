# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 版本相关 API (获取后端版本信息)
# ------------------------------------------------------------

from flask import Blueprint, jsonify

from backend.core.Logger import get_logger
from backend.core.Version import get_version_info

logger = get_logger("API_Version")
version_bp = Blueprint("version", __name__)


@version_bp.route("/", methods=["GET"], strict_slashes=False)
def get_version():
    """获取后端版本信息"""
    version = get_version_info()
    logger.debug(f"获取版本信息: {version}")

    return (
        jsonify(
            {
                "level": "success",
                "data": version,
            },
        ),
        200,
    )
