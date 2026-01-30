# ------------------------------------------------------------
# @author: Churk
# @status: 待审查
# @description: 项目模块
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, session

from backend.config import ROLE_ADMIN
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

    is_admin = False
    if "user_id" in session:
        if session.get("role", 0) >= ROLE_ADMIN:
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

    # 如果是 admin 且请求 all, 则返回所有; 否则只返回公开
    public_only = not (show_all and is_admin)

    projects = project_service.get_all(public_only=public_only)
    projects_list = [project.to_dict() for project in projects]
    return (
        jsonify(
            {
                "level": "success",
                "data": projects_list,
            },
        ),
        200,
    )


@project_bp.route("/<uuid>", methods=["GET"])
def get_project_detail(uuid):
    """获取项目详情"""
    project = project_service.get_by_uuid(uuid)
    if not project:
        return (
            jsonify({"level": "error", "message": "项目不存在"}),
            404,
        )

    # Check permission if not public
    if not project.is_public:
        is_admin = False
        if "user_id" in session:
            if session.get("role", 0) >= ROLE_ADMIN:
                is_admin = True

        if not is_admin:
            return (
                jsonify(
                    {
                        "level": "error",
                        "message": "项目不存在或无权访问",
                    },
                ),
                404,
            )

    return (
        jsonify(
            {
                "level": "success",
                "data": project.to_dict(),
            },
        ),
        200,
    )


@project_bp.route("/", methods=["POST"])
@require_admin
def create_project():
    """创建项目"""
    data = request.json
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

    success, message, project = project_service.create(data)

    if success:
        logger.info(f"项目创建成功: {project.title}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": project.to_dict(),
                },
            ),
            200,
        )
    else:
        logger.error(f"项目创建失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            500,
        )


@project_bp.route("/<uuid>", methods=["PUT"])
@require_admin
def update_project(uuid):
    """更新项目"""
    data = request.json

    success, message, project = project_service.update(uuid, data)

    if success:
        logger.info(f"项目更新成功: {project.title}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": project.to_dict(),
                },
            ),
            200,
        )
    else:
        status_code = 404 if "不存在" in message else 500
        logger.error(f"项目更新失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            status_code,
        )


@project_bp.route("/<uuid>", methods=["DELETE"])
@require_admin
def delete_project(uuid):
    """删除项目"""
    success, message = project_service.delete(uuid)

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
        status_code = 404 if "不存在" in message else 500
        logger.error(f"项目删除失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            status_code,
        )
