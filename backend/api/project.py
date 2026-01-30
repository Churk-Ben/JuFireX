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
    user_role = session.get("role", 0)

    # 代理给 Service, Service 会根据 Role 决定是否真的 view_all
    projects_list = project_service.get_all(user_role=user_role, view_all=show_all)

    # 如果用户想看所有但被 Service 降级了(返回了公开的), 这种行为是静默的，符合 API 设计
    # 但如果用户明确请求 all 且权限不足，原逻辑是返回 403。
    # 为了保持行为一致，我们可以在这里简单判断一下，或者信任 Service 的静默降级。
    # 原逻辑: if show_all and not is_admin: return 403
    # 新逻辑: Service 内部降级。
    # 如果我们要严格保持原 API 行为 (403), 我们需要在 API 层判断。
    # 既然是重构，我们可以稍微放宽，或者为了兼容性，保留 API 层的快速失败。
    # 让我们保留 403 逻辑以保持 API 契约不变，但使用 Service 的接口。

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
    user_role = session.get("role", 0)

    success, message, project = project_service.get_by_uuid(uuid, user_role)

    if not success:
        code = 403 if message == "权限不足" else 404
        return (
            jsonify({"level": "error", "message": message}),
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

    user_role = session.get("role", 0)
    success, message, project = project_service.create(data, user_role)

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


@project_bp.route("/<uuid>", methods=["PUT"])
@require_admin
def update_project(uuid):
    """更新项目"""
    data = request.json
    user_role = session.get("role", 0)

    success, message, project = project_service.update(uuid, data, user_role)

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
        code = 403 if message == "权限不足" else (404 if "不存在" in message else 500)
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
@require_admin
def delete_project(uuid):
    """删除项目"""
    user_role = session.get("role", 0)

    success, message = project_service.delete(uuid, user_role)

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
        code = 403 if message == "权限不足" else (404 if "不存在" in message else 500)
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
