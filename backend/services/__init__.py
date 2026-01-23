from backend.data import users
from .user_service import UserService

user_service = UserService(users)

__all__ = [
    "user_service",
    "UserService",
]
