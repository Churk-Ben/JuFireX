# ------------------------------------------------------------
# @author: Churk
# @status: 完成
# @description: 安全模块
# ------------------------------------------------------------

import functools

from flask import jsonify, session

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
                    jsonify(
                        {
                            "level": "warning",
                            "message": "请先登录",
                        },
                    ),
                    401,
                )

            user_role = session.get("role", ROLE_GUEST)

            if user_role < role:
                return (
                    jsonify(
                        {
                            "level": "warning",
                            "message": "权限不足",
                        },
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_owner(role):
    """
    启用所有者豁免.

    自动检查路由参数中的 `uuid` 或 `user_uuid` 是否与当前登录用户的 UUID 一致.
    如果一致, 或者是role以上权限, 则允许访问. 否则返回 403 错误.

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
                    jsonify(
                        {
                            "level": "warning",
                            "message": "请先登录",
                        },
                    ),
                    401,
                )

            # 1. 检查是否为管理员 (直接放行)
            user_role = session.get("role", ROLE_GUEST)
            if user_role >= role:
                return f(*args, **kwargs)

            # 2. 获取当前用户 UUID
            current_user_uuid = session.get("user_uuid")
            if not current_user_uuid:
                # 这种情况理论上不应该发生, 除非是在添加 user_uuid 之前的旧 session
                # 为了安全起见, 拒绝访问并提示重新登录
                return (
                    jsonify(
                        {
                            "level": "warning",
                            "message": "会话已过期, 请重新登录",
                        },
                    ),
                    401,
                )

            # 3. 获取目标 UUID (从路由参数中)
            # 尝试常见的参数名: uuid, user_uuid
            target_uuid = kwargs.get("uuid") or kwargs.get("user_uuid")

            if target_uuid and target_uuid == current_user_uuid:
                return f(*args, **kwargs)

            # 如果没有匹配到所有者, 且不是管理员
            return (
                jsonify(
                    {
                        "level": "warning",
                        "message": "权限不足",
                    },
                ),
                403,
            )

        return decorated_function

    return decorator(f)


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


def require_owner_or_admin(f):
    """需要所有者权限或管理员以上权限"""
    return require_owner(ROLE_ADMIN)(f)


def require_owner_or_super_admin(f):
    """需要所有者权限或超级管理员以上权限"""
    return require_owner(ROLE_SUPER_ADMIN)(f)
