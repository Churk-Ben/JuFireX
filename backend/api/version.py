# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 版本相关 API (获取后端版本信息)
# ------------------------------------------------------------

import json

from flask import Blueprint, jsonify

from backend.config import Config

version_bp = Blueprint("version", __name__)


@version_bp.route("/", methods=["GET"])
def get_version():
    """获取后端版本信息"""
    ver_json = Config.VERSION_JSON

    if ver_json.exists():
        try:
            with open(ver_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                return jsonify(
                    (
                        {
                            "level": "success",
                            "data": data,
                        },
                    ),
                    200,
                )

        except Exception as e:
            return (
                jsonify(
                    (
                        {
                            "level": "error",
                            "message": f"Failed to read version file: {str(e)}",
                            "data": {
                                "version": "unknown",
                            },
                        },
                    ),
                ),
                500,
            )
    else:
        # 开发环境或未生成版本文件时的回退
        return jsonify(
            (
                {
                    "level": "success",
                    "data": {
                        "version": "dev",
                        "commit_hash": "dev",
                        "branch": "dev",
                        "build_time": "dev",
                        "message": "Development environment",
                    },
                },
            ),
            200,
        )
