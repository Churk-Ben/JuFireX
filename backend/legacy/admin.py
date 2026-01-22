from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    current_app,
    redirect,
    url_for,
)
from .models import db, User
from .config import ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_NAMES
from .utils import require_role, can_manage_user, validate_csrf_token
from .services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__)

# 创建管理员服务实例
admin_service = AdminService(db)


@admin_bp.route("/admin/projects")
@require_role(ROLE_ADMIN)
def admin_projects():
    # 使用服务层获取所有项目
    projects = admin_service.get_all_projects()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "pages/admin/projects.html",
        projects=projects,
        current_user=current_user,
    )


@admin_bp.route("/admin/users")
@require_role(ROLE_ADMIN)
def admin_users():
    # 使用服务层获取所有用户
    users = admin_service.get_all_users()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "pages/admin/users.html",
        users=users,
        current_user=current_user,
        ROLE_NAMES=ROLE_NAMES,
    )


# TODO 改到设置.py
@admin_bp.route("/settings/studio")
@require_role(ROLE_ADMIN)
def admin_studio_info():
    # 使用服务层获取工作室信息
    studio_info = admin_service.get_studio_info()
    current_user = db.session.get(User, session["user_id"])
    return render_template(
        "pages/settings/studio.html",
        studio_info=studio_info,
        current_user=current_user,
    )


@admin_bp.route("/admin/navigation")
@require_role(ROLE_ADMIN)
def admin_navigation():
    current_user = db.session.get(User, session["user_id"])
    
    # 使用服务层获取导航管理数据
    nav_data = admin_service.get_navigation_data(current_user.id)
    
    return render_template(
        "pages/admin/navigations.html",
        current_user=current_user,
        categories=nav_data["categories"],
        nav_items=nav_data["nav_items"],
        hidden_nav_items=nav_data["hidden_nav_items"],
    )


@admin_bp.route("/api/users/<int:user_id>/role", methods=["PUT"])
@require_role(ROLE_ADMIN, owner_check=can_manage_user)
def update_user_role(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.get_json()
    new_role = data.get("role")
    
    # 使用服务层更新用户角色
    success, message = admin_service.update_user_role(user_id, new_role)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({"success": True, "message": message})


@admin_bp.route("/api/users/<int:user_id>/status", methods=["PUT"])
@require_role(ROLE_ADMIN, owner_check=can_manage_user)
def update_user_status(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.get_json()
    new_status = data.get("is_active")

    if new_status is None:
        return jsonify({"success": False, "message": "缺少状态参数"}), 400

    # 使用服务层更新用户状态
    success, message = admin_service.update_user_status(user_id, new_status)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({"success": True, "message": message})


@admin_bp.route("/api/users/<int:user_id>", methods=["GET"])
@require_role(ROLE_ADMIN)
def get_user(user_id):
    # 使用服务层获取用户详情
    user_data = admin_service.get_user_details(user_id)
    
    if not user_data:
        return jsonify({"success": False, "message": "用户不存在"}), 404
        
    return jsonify({"success": True, "user": user_data})


@admin_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@require_role(ROLE_SUPER_ADMIN)
def delete_user(user_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 使用服务层删除用户
    success, message = admin_service.delete_user(user_id, session["user_id"])
    
    if not success:
        # 根据错误消息判断状态码
        if message == "权限不足":
            status_code = 403
        elif message == "不能删除自己的账户":
            status_code = 400
        else:
            status_code = 500
        return jsonify({"success": False, "message": message}), status_code
        
    return jsonify({"success": True, "message": message})


@admin_bp.route("/api/studio-info", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_studio_info():
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.get_json()
    
    # 使用服务层更新工作室信息
    success, message = admin_service.update_studio_info(data)
    
    if not success:
        return jsonify({"success": False, "message": message}), 500
        
    return jsonify({"success": True, "message": message})
