# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航模块
# ------------------------------------------------------------

import json
import os

from flask import Blueprint, jsonify, request, session

from backend.config import Config, ROLE_ADMIN, ROLE_GUEST
from backend.core.Logger import get_logger
from backend.core.Security import require_member, require_login
from backend.services import navigation_service

logger = get_logger("API_Navigation")
nav_bp = Blueprint("navigation", __name__)


@nav_bp.route("/categories", methods=["GET"])
def get_categories():
    """获取所有导航分类"""
    try:
        file_path = Config.NAVIGATIONS_DIR / "categories.json"
        if not os.path.exists(file_path):
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

        with open(file_path, "r", encoding="utf-8") as f:
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
    is_admin = user_role >= ROLE_ADMIN

    # 检查是否请求所有 (管理员)
    show_all = request.args.get("all", "false").lower() == "true"

    if show_all and not is_admin:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "权限不足",
                },
            ),
            403,
        )

    # 如果是管理员明确请求所有, 则 view_all=True, 否则按正常逻辑: 公开 + 自己的
    view_all = show_all and is_admin

    navs = navigation_service.get_all(user_uuid=user_uuid, view_all=view_all)
    navs_list = [nav.to_dict() for nav in navs]

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
    is_admin = user_role >= ROLE_ADMIN

    # 权限控制
    if not is_admin:
        # 如果是成员用户, 强制设置 owner_uuid 为自己
        data["owner_uuid"] = user_uuid
    else:
        # 管理员可以指定 owner_uuid, 如果未指定则默认为 None (系统/公共)
        if "owner_uuid" not in data:
            data["owner_uuid"] = None

    success, message, nav = navigation_service.create(data)

    if success:
        logger.debug(f"导航创建成功: {nav.title}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": nav.to_dict(),
                },
            ),
            201,
        )
    else:
        logger.error(f"导航创建失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            500,
        )


@nav_bp.route("/<uuid>", methods=["PUT"])
@require_login
def update_navigation(uuid):
    """更新导航"""
    data: dict = request.json

    nav = navigation_service.get_by_uuid(uuid)
    if not nav:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "导航不存在",
                },
            ),
            404,
        )

    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)
    is_admin = user_role >= ROLE_ADMIN

    # 如果不是管理员, 且不是所有者 -> 拒绝
    if not is_admin and nav.owner_uuid != user_uuid:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "权限不足",
                },
            ),
            403,
        )

    success, message, nav = navigation_service.update(uuid, data)

    if success:
        logger.debug(f"导航更新成功: {nav.title}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": nav.to_dict(),
                },
            ),
            200,
        )
    else:
        logger.error(f"导航更新失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            500,
        )


@nav_bp.route("/<uuid>", methods=["DELETE"])
@require_login
def delete_navigation(uuid):
    """删除导航"""
    nav = navigation_service.get_by_uuid(uuid)

    if not nav:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "导航不存在",
                },
            ),
            404,
        )

    user_role = session.get("role", ROLE_GUEST)
    is_admin = user_role >= ROLE_ADMIN
    user_uuid = session.get("user_uuid")

    # 如果不是管理员, 且不是所有者 -> 拒绝
    if not is_admin and nav.owner_uuid != user_uuid:
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "权限不足",
                },
            ),
            403,
        )

    success, message = navigation_service.delete(uuid)

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
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            500,
        )
