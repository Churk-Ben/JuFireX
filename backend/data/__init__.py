# Unified Data Access Layer
# Expose repositories as singleton instances or classes for easy access

from .repositories.user_repo import UserRepository
from .repositories.nav_repo import NavCategoryRepository, NavItemRepository
from .repositories.project_repo import ProjectRepository
from .repositories.blog_repo import BlogRepository

# Instantiate repositories
users = UserRepository()
nav_categories = NavCategoryRepository()
nav_items = NavItemRepository()
projects = ProjectRepository()
blogs = BlogRepository()

__all__ = [
    "users",
    "nav_categories",
    "nav_items",
    "projects",
    "blogs",
    "UserRepository",
    "NavCategoryRepository",
    "NavItemRepository",
    "ProjectRepository",
    "BlogRepository",
]
