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
                # 尝试从数据库刷新权限 (处理 Session 过期/未更新的情况)
                user_uuid = session.get("user_uuid")
                if user_uuid:
                    try:
                        from backend.data.database import db
                        from backend.data.models.user import User
                        from sqlalchemy import select

                        stmt = select(User).where(User.uuid == user_uuid)
                        user_obj = db.session.execute(stmt).scalars().first()

                        if user_obj and user_obj.role >= role:
                            # 更新 Session 并放行
                            session["role"] = user_obj.role
                            return f(*args, **kwargs)
                    except Exception:
                        pass

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


def require_self_or_role(role):
    """
    启用"本人或指定角色"鉴权 (Identity Match OR Role Check).

    用于操作用户自身的接口 (如修改密码, 重建目录).
    允许访问的条件:
    1. 当前用户拥有 >= role 的角色权限.
    2. 或者当前用户就是被操作的目标用户 (uuid一致).

    Args:
        role (int): 豁免所需的最低角色等级 (如果不是本人, 需要达到此等级).

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

            # 1. 检查是否为特权角色 (直接放行)
            user_role = session.get("role", ROLE_GUEST)
            if user_role >= role:
                return f(*args, **kwargs)

            # 2. 获取当前用户 UUID
            current_user_uuid = session.get("user_uuid")
            if not current_user_uuid:
                return (
                    jsonify(
                        {
                            "level": "warning",
                            "message": "会话已过期, 请重新登录",
                        },
                    ),
                    401,
                )

            # 3. 获取目标 UUID (待操作的用户 UUID)
            target_uuid = kwargs.get("uuid") or kwargs.get("user_uuid")
            if not target_uuid and request.is_json:
                data = request.get_json(silent=True) or {}
                target_uuid = data.get("uuid") or data.get("user_uuid")

            if target_uuid and target_uuid == current_user_uuid:
                return f(*args, **kwargs)

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


def require_self(f):
    """需要本人权限 (Strict Self Check)"""
    return require_self_or_role(ROLE_SUPER_ADMIN + 999)(f)


def require_self_or_admin(f):
    """需要本人权限或管理员以上权限"""
    return require_self_or_role(ROLE_ADMIN)(f)


def require_self_or_super_admin(f):
    """需要本人权限或超级管理员以上权限"""
    return require_self_or_role(ROLE_SUPER_ADMIN)(f)
