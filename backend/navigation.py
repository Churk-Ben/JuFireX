from flask import Blueprint, render_template, request, jsonify, session
from .models import db, User
from .config import ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_GUEST
from .utils import require_role, can_manage_nav_item, validate_csrf_token
from .services.navigation_service import NavigationService

navigation_bp = Blueprint("navigation", __name__)

# 创建导航服务实例
navigation_service = NavigationService(db)


@navigation_bp.route("/navigation")
@require_role(ROLE_GUEST)
def navigation():
    current_user = db.session.get(User, session.get("user_id"))
    user_id = current_user.id if current_user else None
    
    # 使用服务层获取用户导航数据
    nav_data = navigation_service.get_user_navigation(user_id)
    
    return render_template(
        "pages/navigations.html",
        categories=nav_data["categories"],
        current_user=current_user,
        hidden_nav_items=nav_data["hidden_nav_items"],
        nav_items_by_category=nav_data["nav_items_by_category"],
    )


@navigation_bp.route("/api/navigation/hide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def hide_nav_item(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user_id = session["user_id"]
    
    # 使用服务层隐藏导航项
    success, message = navigation_service.hide_nav_item(user_id, nav_item_id)
    
    return jsonify({"success": success, "message": message})


@navigation_bp.route("/api/navigation/unhide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def unhide_nav_item(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user_id = session["user_id"]
    
    # 使用服务层显示导航项
    success, message = navigation_service.unhide_nav_item(user_id, nav_item_id)
    
    return jsonify({"success": success, "message": message})


@navigation_bp.route("/api/navigation/unhide_all", methods=["POST"])
@require_role(ROLE_MEMBER)
def unhide_all_nav_items():
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user_id = session["user_id"]
    
    # 使用服务层显示所有导航项
    success, message = navigation_service.unhide_all_nav_items(user_id)
    
    return jsonify({"success": success, "message": message})


@navigation_bp.route(
    "/api/navigation/toggle_privacy/<int:nav_item_id>", methods=["POST"]
)
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def toggle_nav_item_privacy(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403
    
    # 使用服务层切换导航项私有状态
    success, message, _ = navigation_service.toggle_nav_item_privacy(nav_item_id)
    
    return jsonify({"success": success, "message": message})


@navigation_bp.route("/api/nav-categories", methods=["GET"])
@require_role(ROLE_GUEST)
def get_nav_categories():
    # 使用服务层获取所有导航分类
    categories = navigation_service.get_navigation_data()["categories"]
    
    categories_data = []
    for category in categories:
        categories_data.append(
            {
                "id": category.id,
                "name": category.name,
                "order": category.order,
                "created_at": category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return jsonify({"success": True, "categories": categories_data})


@navigation_bp.route("/api/nav-categories", methods=["POST"])
@require_role(ROLE_ADMIN)
def create_nav_category():
    data = request.get_json()
    name = data.get("name")
    order = data.get("order", 0)

    if not name:
        return jsonify({"success": False, "message": "分类名称不能为空"}), 400

    # 使用服务层创建导航分类
    success, message, category_data = navigation_service.create_nav_category(name, order)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400

    return jsonify(
        {
            "success": True,
            "message": message,
            "category": category_data,
        }
    )


@navigation_bp.route("/api/nav-categories/<int:category_id>", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_nav_category(category_id):
    data = request.get_json()
    name = data.get("name")
    order = data.get("order")
    
    # 使用服务层更新导航分类
    success, message, category_data = navigation_service.update_nav_category(category_id, name, order)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({
        "success": True,
        "message": message,
        "category": category_data
    })


@navigation_bp.route("/api/nav-categories/<int:category_id>", methods=["DELETE"])
@require_role(ROLE_ADMIN)
def delete_nav_category(category_id):
    # 使用服务层删除导航分类
    success, message = navigation_service.delete_nav_category(category_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400

    return jsonify({"success": True, "message": message})


@navigation_bp.route("/api/nav-items", methods=["GET"])
@require_role(ROLE_GUEST)
def get_nav_items():
    category_id = request.args.get("category_id", type=int)
    
    # 使用服务层获取导航项
    nav_items = navigation_service.get_nav_items(category_id)

    items_data = []
    for item in nav_items:
        items_data.append(
            {
                "id": item.id,
                "title": item.title,
                "url": item.url,
                "description": item.description,
                "icon": item.icon,
                "order": item.order,
                "is_public": item.is_public,
                "category_id": item.category_id,
                "category_name": item.category.name,
                "creator_id": item.created_by,
                "creator_name": item.creator.username if item.creator else None,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify({"success": True, "items": items_data})


@navigation_bp.route("/api/nav-items", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_nav_item():
    data = request.get_json()
    user_id = session.get("user_id")
    
    # 使用服务层创建导航项
    success, message, item_data = navigation_service.create_nav_item(data, user_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({
        "success": True,
        "message": message,
        "item": item_data
    })


@navigation_bp.route("/api/nav-items/<int:item_id>", methods=["GET"])
@require_role(ROLE_MEMBER)
def get_nav_item(item_id):
    user_id = session["user_id"]
    
    # 使用服务层获取单个导航项
    success, message, item_data = navigation_service.get_nav_item(item_id, user_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 403

    return jsonify({"success": True, "item": item_data})


@navigation_bp.route("/api/nav-items/<int:item_id>", methods=["PUT"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def update_nav_item(item_id):
    data = request.get_json()
    user_id = session.get("user_id")
    
    # 使用服务层更新导航项
    success, message, item_data = navigation_service.update_nav_item(item_id, data, user_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({
        "success": True,
        "message": message,
        "item": item_data
    })


@navigation_bp.route("/api/nav-items/<int:item_id>", methods=["DELETE"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def delete_nav_item(item_id):
    user_id = session.get("user_id")
    
    # 使用服务层删除导航项
    success, message = navigation_service.delete_nav_item(item_id, user_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 400
        
    return jsonify({"success": True, "message": message})


@navigation_bp.route("/api/nav-items/<int:item_id>/visibility", methods=["PUT"])
@require_role(ROLE_MEMBER)
def toggle_nav_item_visibility(item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.get_json()
    is_public = data.get("is_public")
    user_id = session["user_id"]

    # 使用服务层切换导航项可见性
    success, message = navigation_service.toggle_nav_item_visibility(item_id, is_public, user_id)
    
    if not success:
        return jsonify({"success": False, "message": message}), 403
        
    return jsonify({"success": True, "message": message})
