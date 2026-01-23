# 将所有数据访问层组件组织在一个模块中, 方便统一管理和维护.

from .repositories.user_repo import UserRepository

# 导出 UserRepository 实例, 用于在应用中直接使用
users = UserRepository()

__all__ = [
    "users",
    "UserRepository",
]
