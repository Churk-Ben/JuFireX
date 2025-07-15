from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session
from .models import db, User, Project, StudioInfo, NavCategory, NavItem, HiddenNavItem
from .config import (
    ROLE_GUEST,
    ROLE_MEMBER,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
    ROLE_NAMES,
)
from .utils import require_role, can_manage_user, validate_csrf_token

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/projects")
@require_role(ROLE_ADMIN)
def admin_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "admin/projects.html", projects=projects, current_user=current_user
    )


@admin_bp.route("/admin/users")
@require_role(ROLE_ADMIN)
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "admin/users.html",
        users=users,
        current_user=current_user,
        ROLE_NAMES=ROLE_NAMES,
    )


@admin_bp.route("/admin/studio-info")
@require_role(ROLE_ADMIN)
def admin_studio_info():
    studio_info = StudioInfo.query.first()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "admin/studio_info.html", studio_info=studio_info, current_user=current_user
    )


@admin_bp.route("/admin/navigation")
@require_role(ROLE_ADMIN)
def admin_navigation():
    current_user = db.session.get(User, session["user_id"])
    # 获取所有分类和导航项
    categories = NavCategory.query.order_by(NavCategory.order).all()
    nav_items = NavItem.query.order_by(NavItem.order).all()

    # 获取当前用户隐藏的导航项
    hidden_items = (
        db.session.query(HiddenNavItem, NavItem)
        .join(NavItem, HiddenNavItem.nav_item_id == NavItem.id)
        .filter(HiddenNavItem.user_id == current_user.id)
        .all()
    )

    hidden_nav_items = []
    for hidden_item, nav_item in hidden_items:
        hidden_nav_items.append(
            {
                "id": nav_item.id,
                "title": nav_item.title,
                "url": nav_item.url,
                "description": nav_item.description,
                "icon": nav_item.icon,
                "category_id": nav_item.category_id,
                "category_name": nav_item.category.name,
                "hidden_at": hidden_item.hidden_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return render_template(
        "admin/navigation.html",
        current_user=current_user,
        categories=categories,
        nav_items=nav_items,
        hidden_nav_items=hidden_nav_items,
    )


@admin_bp.route("/api/users/<int:user_id>/role", methods=["PUT"])
@require_role(ROLE_ADMIN, owner_check=can_manage_user)
def update_user_role(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in [ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN]:
        return jsonify({"success": False, "message": "无效的角色"}), 400

    user.role = new_role
    db.session.commit()

    return jsonify({"success": True, "message": "用户角色更新成功"})


@admin_bp.route("/api/users/<int:user_id>/status", methods=["PUT"])
@require_role(ROLE_ADMIN, owner_check=can_manage_user)
def update_user_status(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_status = data.get("is_active")

    if new_status is None:
        return jsonify({"success": False, "message": "缺少状态参数"}), 400

    user.is_active = new_status
    db.session.commit()

    status_text = "激活" if new_status else "禁用"
    return jsonify({"success": True, "message": f"用户已{status_text}"})


@admin_bp.route("/api/users/<int:user_id>", methods=["GET"])
@require_role(ROLE_ADMIN)
def get_user(user_id):
    user = User.query.get_or_404(user_id)

    # 构建用户数据
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "role_name": ROLE_NAMES.get(user.role, "未知"),
        "is_active": user.is_active,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "avatar_path": user.avatar_path,
    }

    return jsonify({"success": True, "user": user_data})


@admin_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@require_role(ROLE_SUPER_ADMIN)
def delete_user(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user = User.query.get_or_404(user_id)

    # 不能删除自己
    if user.id == session["user_id"]:
        return jsonify({"success": False, "message": "不能删除自己的账户"}), 400

    # 不能删除其他超级管理员（除非是超级管理员删除普通管理员）
    current_user = db.session.get(User, session["user_id"])
    if user.role == ROLE_SUPER_ADMIN and current_user.role != ROLE_SUPER_ADMIN:
        return jsonify({"success": False, "message": "权限不足"}), 403

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "用户已删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500


@admin_bp.route("/api/studio-info", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_studio_info():
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    try:
        data = request.get_json()
        studio_info = StudioInfo.query.first()

        if not studio_info:
            # 如果不存在，创建新的
            studio_info = StudioInfo(
                name=data.get("name", ""),
                description=data.get("description", ""),
                logo_url=data.get("logo_url", ""),
                contact_email=data.get("contact_email", ""),
                github_url=data.get("github_url", ""),
            )
            db.session.add(studio_info)
        else:
            # 更新现有信息
            studio_info.name = data.get("name", studio_info.name)
            studio_info.description = data.get("description", studio_info.description)
            studio_info.logo_url = data.get("logo_url", studio_info.logo_url)
            studio_info.contact_email = data.get(
                "contact_email", studio_info.contact_email
            )
            studio_info.github_url = data.get("github_url", studio_info.github_url)
            studio_info.updated_at = datetime.now()

        db.session.commit()
        return jsonify({"success": True, "message": "工作室信息更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500
