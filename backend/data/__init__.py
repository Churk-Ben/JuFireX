# Unified Data Access Layer
# Expose repositories as singleton instances or classes for easy access

from .repositories.user_repo import UserRepository

# Instantiate repositories
users = UserRepository()

__all__ = [
    "users",
    "UserRepository",
]
