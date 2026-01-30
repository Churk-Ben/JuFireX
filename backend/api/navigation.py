# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航模块
# ------------------------------------------------------------

import json

from flask import Blueprint, jsonify, request, session

from backend.config import Config, ROLE_ADMIN, ROLE_GUEST
from backend.core.Logger import get_logger
from backend.core.Security import require_login, require_member
from backend.services import navigation_service

logger = get_logger("API_Navigation")
nav_bp = Blueprint("navigation", __name__)


@nav_bp.route("/categories", methods=["GET"])
def get_categories():
    """获取所有导航分类"""
    try:
        file_path = Config.NAVIGATIONS_DIR / "categories.json"
        if not file_path.exists():
            logger.warning("获取分类文件时发现文件不存在, 建议检查返回结果是否可靠")
            return (
                jsonify(
                    {
                        "level": "success",
                        "data": [],
                    },
                ),
                200,
            )

        with file_path.open("r", encoding="utf-8") as f:
            categories = json.load(f)

        logger.debug(f"获取分类文件成功, 现有分类: {categories}")
        return (
            jsonify(
                {
                    "level": "success",
                    "data": categories,
                },
            ),
            200,
        )
    except Exception as e:
        logger.error(f"获取分类失败: {e}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "获取分类失败",
                },
            ),
            500,
        )


@nav_bp.route("/", methods=["GET"])
def get_navigations():
    """获取导航列表"""
    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    # 检查是否请求所有 (管理员)
    show_all = request.args.get("all", "false").lower() == "true"

    if show_all and user_role < ROLE_ADMIN:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "权限不足",
                },
            ),
            403,
        )

    navs_list = navigation_service.get_all(
        user_uuid=user_uuid, user_role=user_role, view_all=show_all
    )

    return (
        jsonify(
            {
                "level": "success",
                "data": navs_list,
            },
        ),
        200,
    )


@nav_bp.route("/", methods=["POST"])
@require_member
def create_navigation():
    """创建导航"""
    data: dict = request.json
    if not data or not data.get("title") or not data.get("url"):
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "标题和链接不能为空",
                },
            ),
            400,
        )

    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    success, message, nav = navigation_service.create(data, user_uuid, user_role)

    if success:
        logger.debug(f"导航创建成功: {nav.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": nav,
                },
            ),
            201,
        )
    else:
        logger.error(f"导航创建失败: {message}")
        code = 403 if message == "权限不足" else 500
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )


@nav_bp.route("/<uuid>", methods=["PUT"])
@require_login
def update_navigation(uuid):
    """更新导航"""
    data: dict = request.json

    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    success, message, nav = navigation_service.update(uuid, data, user_uuid, user_role)

    if success:
        logger.debug(f"导航更新成功: {nav.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": nav,
                },
            ),
            200,
        )
    else:
        logger.error(f"导航更新失败: {message}")
        code = (
            403 if message == "权限不足" else (404 if message == "导航不存在" else 500)
        )
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )


@nav_bp.route("/<uuid>", methods=["DELETE"])
@require_login
def delete_navigation(uuid):
    """删除导航"""
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")

    success, message = navigation_service.delete(uuid, user_uuid, user_role)

    if success:
        logger.debug(f"导航删除成功: {uuid}")
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
        logger.error(f"导航删除失败: {message}")
        code = (
            403 if message == "权限不足" else (404 if message == "导航不存在" else 500)
        )
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )
