from flask import Blueprint, render_template, request, jsonify, session
from .models import db, NavCategory, NavItem, HiddenNavItem, User
from .config import ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_GUEST
from .utils import require_role, can_manage_nav_item, validate_csrf_token

navigation_bp = Blueprint("navigation", __name__)


@navigation_bp.route("/navigation")
@require_role(ROLE_GUEST)
def navigation():
    # 获取所有分类和导航项
    categories = NavCategory.query.order_by(NavCategory.order).all()
    current_user = db.session.get(User, session.get("user_id"))

    # 获取当前用户隐藏的导航项
    hidden_nav_items = set()
    if current_user:
        hidden_items = HiddenNavItem.query.filter_by(user_id=current_user.id).all()
        hidden_nav_items = {item.nav_item_id for item in hidden_items}

    # 获取所有导航项并按分类分组
    nav_items_by_category = {}
    for category in categories:
        # 获取该分类下的所有导航项（排除隐藏的）
        nav_items = NavItem.query.filter_by(category_id=category.id).filter(
            ~NavItem.id.in_(hidden_nav_items) if hidden_nav_items else True
        ).order_by(NavItem.order).all()
        
        if nav_items:
            nav_items_by_category[category.id] = nav_items

    return render_template(
        "navigation.html",
        categories=categories,
        current_user=current_user,
        hidden_nav_items=hidden_nav_items,
        nav_items_by_category=nav_items_by_category,
    )


@navigation_bp.route("/api/navigation/hide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def hide_nav_item(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user_id = session["user_id"]

    # 检查是否已经隐藏
    existing = HiddenNavItem.query.filter_by(
        user_id=user_id, nav_item_id=nav_item_id
    ).first()
    if existing:
        return jsonify({"success": False, "message": "该导航项已被隐藏"})

    # 添加隐藏记录
    hidden_item = HiddenNavItem(user_id=user_id, nav_item_id=nav_item_id)
    db.session.add(hidden_item)
    db.session.commit()

    return jsonify({"success": True, "message": "导航项已隐藏"})


@navigation_bp.route("/api/navigation/unhide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def unhide_nav_item(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    user_id = session["user_id"]

    # 查找并删除隐藏记录
    hidden_item = HiddenNavItem.query.filter_by(
        user_id=user_id, nav_item_id=nav_item_id
    ).first()
    if not hidden_item:
        return jsonify({"success": False, "message": "该导航项未被隐藏"})

    db.session.delete(hidden_item)
    db.session.commit()

    return jsonify({"success": True, "message": "导航项已显示"})


@navigation_bp.route("/api/navigation/toggle_privacy/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def toggle_nav_item_privacy(nav_item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    nav_item = NavItem.query.get_or_404(nav_item_id)
    nav_item.is_private = not nav_item.is_private
    db.session.commit()

    status = "私有" if nav_item.is_private else "公开"
    return jsonify({"success": True, "message": f"导航项已设为{status}"})


@navigation_bp.route("/api/navigation/hidden_items", methods=["GET"])
@require_role(ROLE_MEMBER)
def get_hidden_nav_items():
    user_id = session["user_id"]
    hidden_items = (
        db.session.query(HiddenNavItem, NavItem)
        .join(NavItem, HiddenNavItem.nav_item_id == NavItem.id)
        .filter(HiddenNavItem.user_id == user_id)
        .all()
    )

    items_data = []
    for hidden_item, nav_item in hidden_items:
        items_data.append(
            {
                "id": nav_item.id,
                "title": nav_item.title,
                "url": nav_item.url,
                "category_id": nav_item.category_id,
                "category_name": nav_item.category.name,
            }
        )

    return jsonify({"success": True, "items": items_data})


@navigation_bp.route("/api/nav-categories", methods=["GET"])
@require_role(ROLE_GUEST)
def get_nav_categories():
    categories = NavCategory.query.order_by(NavCategory.order).all()
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

    # 检查名称是否已存在
    existing = NavCategory.query.filter_by(name=name).first()
    if existing:
        return jsonify({"success": False, "message": "分类名称已存在"}), 400

    category = NavCategory(name=name, order=order)
    db.session.add(category)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "分类创建成功",
            "category": {
                "id": category.id,
                "name": category.name,
                "order": category.order,
                "created_at": category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }
    )


@navigation_bp.route("/api/nav-categories/<int:category_id>", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_nav_category(category_id):
    category = NavCategory.query.get_or_404(category_id)
    data = request.get_json()

    name = data.get("name")
    order = data.get("order")

    if name:
        # 检查名称是否已存在（排除当前分类）
        existing = (
            NavCategory.query.filter_by(name=name).filter(NavCategory.id != category_id).first()
        )
        if existing:
            return jsonify({"success": False, "message": "分类名称已存在"}), 400
        category.name = name

    if order is not None:
        category.order = order

    db.session.commit()

    return jsonify({"success": True, "message": "分类更新成功"})


@navigation_bp.route("/api/nav-categories/<int:category_id>", methods=["DELETE"])
@require_role(ROLE_ADMIN)
def delete_nav_category(category_id):
    category = NavCategory.query.get_or_404(category_id)

    # 检查是否有关联的导航项
    nav_items_count = NavItem.query.filter_by(category_id=category_id).count()
    if nav_items_count > 0:
        return (
            jsonify({"success": False, "message": "该分类下还有导航项，无法删除"}),
            400,
        )

    db.session.delete(category)
    db.session.commit()

    return jsonify({"success": True, "message": "分类删除成功"})


@navigation_bp.route("/api/nav-items", methods=["GET"])
@require_role(ROLE_GUEST)
def get_nav_items():
    category_id = request.args.get("category_id", type=int)
    if category_id:
        nav_items = NavItem.query.filter_by(category_id=category_id).order_by(NavItem.order).all()
    else:
        nav_items = NavItem.query.order_by(NavItem.order).all()

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
                "is_private": item.is_private,
                "category_id": item.category_id,
                "category_name": item.category.name,
                "creator_id": item.creator_id,
                "creator_name": item.creator.username if item.creator else None,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify({"success": True, "items": items_data})


@navigation_bp.route("/api/nav-items", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_nav_item():
    data = request.get_json()
    title = data.get("title")
    url = data.get("url")
    description = data.get("description", "")
    icon = data.get("icon", "")
    order = data.get("order", 0)
    is_private = data.get("is_private", False)
    category_id = data.get("category_id")

    if not title or not url or not category_id:
        return jsonify({"success": False, "message": "标题、链接和分类不能为空"}), 400

    # 验证分类是否存在
    category = NavCategory.query.get(category_id)
    if not category:
        return jsonify({"success": False, "message": "指定的分类不存在"}), 400

    nav_item = NavItem(
        title=title,
        url=url,
        description=description,
        icon=icon,
        order=order,
        is_private=is_private,
        category_id=category_id,
        creator_id=session["user_id"],
    )
    db.session.add(nav_item)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "导航项创建成功",
            "item": {
                "id": nav_item.id,
                "title": nav_item.title,
                "url": nav_item.url,
                "description": nav_item.description,
                "icon": nav_item.icon,
                "order": nav_item.order,
                "is_private": nav_item.is_private,
                "category_id": nav_item.category_id,
                "category_name": nav_item.category.name,
                "creator_id": nav_item.creator_id,
                "creator_name": nav_item.creator.username,
                "created_at": nav_item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }
    )


@navigation_bp.route("/api/nav-items/<int:item_id>", methods=["PUT"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def update_nav_item(item_id):
    nav_item = NavItem.query.get_or_404(item_id)
    data = request.get_json()

    # 更新字段
    if "title" in data:
        nav_item.title = data["title"]
    if "url" in data:
        nav_item.url = data["url"]
    if "description" in data:
        nav_item.description = data["description"]
    if "icon" in data:
        nav_item.icon = data["icon"]
    if "order" in data:
        nav_item.order = data["order"]
    if "is_private" in data:
        nav_item.is_private = data["is_private"]
    if "category_id" in data:
        # 验证分类是否存在
        category = NavCategory.query.get(data["category_id"])
        if not category:
            return jsonify({"success": False, "message": "指定的分类不存在"}), 400
        nav_item.category_id = data["category_id"]

    db.session.commit()

    return jsonify({"success": True, "message": "导航项更新成功"})


@navigation_bp.route("/api/nav-items/<int:item_id>", methods=["DELETE"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def delete_nav_item(item_id):
    nav_item = NavItem.query.get_or_404(item_id)

    # 删除相关的隐藏记录
    HiddenNavItem.query.filter_by(nav_item_id=item_id).delete()

    # 删除导航项
    db.session.delete(nav_item)
    db.session.commit()

    return jsonify({"success": True, "message": "导航项删除成功"})


@navigation_bp.route("/api/nav-items/<int:item_id>/visibility", methods=["PUT"])
@require_role(ROLE_MEMBER)
def toggle_nav_item_visibility(item_id):
    # 验证 CSRF token
    if not validate_csrf_token():
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.get_json()
    action = data.get("action")  # 'toggle_privacy' 或 'toggle_hidden'
    user_id = session["user_id"]

    if action == "toggle_privacy":
        # 切换公开/私有状态（仅限创建者或超级管理员）
        nav_item = NavItem.query.get_or_404(item_id)
        user = db.session.get(User, user_id)

        if nav_item.creator_id != user_id and user.role < ROLE_SUPER_ADMIN:
            return jsonify({"success": False, "message": "只有创建者或超级管理员可以修改隐私设置"}), 403

        nav_item.is_private = not nav_item.is_private
        db.session.commit()

        status = "私有" if nav_item.is_private else "公开"
        return jsonify({"success": True, "message": f"导航项已设为{status}"})

    elif action == "toggle_hidden":
        # 切换隐藏/显示状态（个人设置）
        hidden_item = HiddenNavItem.query.filter_by(
            user_id=user_id, nav_item_id=item_id
        ).first()

        if hidden_item:
            # 当前已隐藏，取消隐藏
            db.session.delete(hidden_item)
            message = "导航项已显示"
        else:
            # 当前未隐藏，添加隐藏
            hidden_item = HiddenNavItem(user_id=user_id, nav_item_id=item_id)
            db.session.add(hidden_item)
            message = "导航项已隐藏"

        db.session.commit()
        return jsonify({"success": True, "message": message})

    else:
        return jsonify({"success": False, "message": "无效的操作类型"}), 400