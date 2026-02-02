# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 博客模块
# ------------------------------------------------------------

from flask import Blueprint, jsonify, request, session

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.core.Logger import get_logger
from backend.core.Security import require_member
from backend.services import blog_service

logger = get_logger("API_Blog")
blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/", methods=["GET"])
def get_blogs():
    """
    @name: 获取博客列表
    @expect: None
    @return:
    {
        "level": "success",
        "data": [
            blog_obj...
        ]
    }
    """
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

    blogs = blog_service.get_all(user_uuid=user_uuid, view_all=view_all)
    return (
        jsonify(
            {
                "level": "success",
                "data": blogs,
            },
        ),
        200,
    )


@blog_bp.route("/<uuid>", methods=["GET"])
def get_blog_detail(uuid):
    """获取博客详情"""
    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    success, message, blog = blog_service.get_by_uuid(uuid, user_uuid, user_role)

    if not success:
        # 如果是权限不足, 返回 403; 如果是不存在, 返回 404
        # 为了安全, 也可以统一返回 404, 但这里为了清晰区分, 使用 403
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

    # 增加访问量并更新视图数
    blog_service.increment_views(uuid)
    blog["views"] = blog.get("views", 0) + 1

    return (
        jsonify(
            {
                "level": "success",
                "data": blog,
            },
        ),
        200,
    )


@blog_bp.route("/", methods=["POST"])
@require_member
def create_blog():
    """
    @name: 创建博客
    """
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

    # 自动填充所有者信息
    if "user_uuid" in session:
        data["owner_uuid"] = session["user_uuid"]

    if not data.get("owner_uuid"):
        return (
            jsonify(
                {
                    "level": "error",
                    "message": "无法获取用户身份",
                },
            ),
            401,
        )

    success, message, blog = blog_service.create(data)

    if success:
        logger.debug(f"文章创建成功: {blog.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": blog,
                },
            ),
            200,
        )
    else:
        logger.error(f"文章创建失败: {message}")
        return (
            jsonify(
                {
                    "level": "error",
                    "message": message,
                },
            ),
            500,
        )


@blog_bp.route("/<uuid>", methods=["PUT"])
@require_member
def update_blog(uuid):
    """更新博客"""
    data: dict = request.json
    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    success, message, blog = blog_service.update(uuid, data, user_uuid, user_role)

    if success:
        logger.debug(f"文章 {blog.get('uuid')} 更新成功: {blog.get('title')}")
        return (
            jsonify(
                {
                    "level": "success",
                    "message": message,
                    "data": blog,
                },
            ),
            200,
        )
    else:
        logger.error(f"文章更新失败: {message}")
        code = (
            403 if message == "权限不足" else (404 if message == "文章不存在" else 500)
        )
        level = "warning" if code < 500 else "error"
        return (
            jsonify(
                {
                    "level": level,
                    "message": message,
                },
            ),
            code,
        )


@blog_bp.route("/<uuid>", methods=["DELETE"])
@require_member
def delete_blog(uuid):
    """删除博客"""
    user_uuid = session.get("user_uuid")
    user_role = session.get("role", ROLE_GUEST)

    success, message = blog_service.delete(uuid, user_uuid, user_role)

    if success:
        logger.debug(f"文章删除成功: {uuid}")
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
        logger.error(f"文章删除失败: {message}")
        code = (
            403 if message == "权限不足" else (404 if message == "文章不存在" else 500)
        )
        level = "warning" if code < 500 else "error"
        return (
            jsonify(
                {
                    "level": level,
                    "message": message,
                },
            ),
            code,
        )
