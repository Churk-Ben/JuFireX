from .repositories.user_repo import UserRepository

users = UserRepository()

__all__ = [
    "users",
    "UserRepository",
]
