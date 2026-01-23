# ------------------------------
# @author: Churk
# @description: 安全模块
# ------------------------------

import functools

from flask import jsonify, current_app, session

from backend.config import ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN


def require_role(role):
    """
    装饰器, 检查当前用户是否有足够的权限.

    如果用户未登录, 返回 401 错误.
    如果用户角色低于所需角色, 返回 403 错误.

    Args:
        role (int): 所需的角色等级.

    Returns:
        function: 包装后的函数.
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return (
                    jsonify({"level": "warning", "message": "请先登录"}),
                    401,
                )

            user_role = session.get("role", ROLE_GUEST)

            if user_role < role:
                return (
                    jsonify({"level": "warning", "message": "权限不足"}),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_login(f):
    """需要登录"""
    return require_role(ROLE_GUEST)(f)


def require_member(f):
    """需要成员权限"""
    return require_role(ROLE_MEMBER)(f)


def require_admin(f):
    """需要管理员权限"""
    return require_role(ROLE_ADMIN)(f)


def require_super_admin(f):
    """需要超级管理员权限"""
    return require_role(ROLE_SUPER_ADMIN)(f)
