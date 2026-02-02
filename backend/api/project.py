# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 项目模块
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, session

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.core.Logger import get_logger
from backend.core.Security import require_admin
from backend.services import project_service

logger = get_logger("API_Project")
project_bp = Blueprint("project", __name__)


@project_bp.route("/", methods=["GET"])
def get_projects():
    """获取项目列表"""
    # 检查是否请求所有 (管理员)
    show_all = request.args.get("all", "false").lower() == "true"

    user_uuid = session.get("user_uuid")
    is_admin = False
    if "user_id" in session:
        if session.get("role", ROLE_GUEST) >= ROLE_ADMIN:
            is_admin = True

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

    projects = project_service.get_all(user_uuid=user_uuid, view_all=view_all)
    return (
        jsonify(
            {
                "level": "success",
                "data": projects,
            },
        ),
        200,
    )


@project_bp.route("/<uuid>", methods=["GET"])
def get_project_detail(uuid):
    """获取项目详情 (Overview)"""
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")

    success, message, project = project_service.get_by_uuid(uuid, user_role, user_uuid)

    if not success:
        code = 403 if message == "权限不足" else 404
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )

    return (
        jsonify(
            {
                "level": "success",
                "data": project,
            },
        ),
        200,
    )


@project_bp.route("/<uuid>/files", methods=["GET"])
def get_project_files(uuid):
    """获取项目文件列表"""
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")
    path = request.args.get("path", "")

    success, message, files = project_service.get_file_tree(
        uuid, path, user_role, user_uuid
    )

    if not success:
        code = 403 if message == "权限不足" else (404 if "不存在" in message else 500)
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )

    return (
        jsonify(
            {
                "level": "success",
                "data": files,
            },
        ),
        200,
    )


@project_bp.route("/<uuid>/file", methods=["GET"])
def get_file_content(uuid):
    """获取文件内容"""
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")
    path = request.args.get("path", "")

    if not path:
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "路径不能为空",
                },
            ),
            400,
        )

    success, message, content = project_service.get_file_content(
        uuid, path, user_role, user_uuid
    )

    if not success:
        code = 403 if message == "权限不足" else (404 if "不存在" in message else 500)
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )

    return (
        jsonify(
            {
                "level": "success",
                "data": content,
            },
        ),
        200,
    )


@project_bp.route("/", methods=["POST"])
def create_project():
    """创建项目"""
    data: dict = request.json
    if not data or not data.get("title"):
        return (
            jsonify(
                {
                    "level": "warning",
                    "message": "标题不能为空",
                },
            ),
            400,
        )

    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")

    success, message, project = project_service.create(data, user_uuid, user_role)

    if success:
        logger.info(f"项目创建成功: {project.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": project,
                },
            ),
            200,
        )
    else:
        logger.error(f"项目创建失败: {message}")
        code = 403 if "权限不足" in message else 500
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )


@project_bp.route("/<uuid>", methods=["PUT"])
def update_project(uuid):
    """更新项目"""
    data: dict = request.json
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")

    success, message, project = project_service.update(uuid, data, user_role, user_uuid)

    if success:
        logger.info(f"项目更新成功: {project.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": project,
                },
            ),
            200,
        )
    else:
        code = 403 if "权限不足" in message else (404 if "不存在" in message else 500)
        logger.error(f"项目更新失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )


@project_bp.route("/<uuid>", methods=["DELETE"])
def delete_project(uuid):
    """删除项目"""
    user_role = session.get("role", ROLE_GUEST)
    user_uuid = session.get("user_uuid")

    success, message = project_service.delete(uuid, user_role, user_uuid)

    if success:
        logger.info(f"项目删除成功: {uuid}")
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
        code = 403 if "权限不足" in message else (404 if "不存在" in message else 500)
        logger.error(f"项目删除失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            code,
        )
