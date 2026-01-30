from backend.data import blogs, navigations, projects, users

from .blog_service import BlogService
from .navigation_service import NavigationService
from .project_service import ProjectService
from .user_service import UserService

user_service = UserService(users)
navigation_service = NavigationService(navigations)
project_service = ProjectService(projects)
blog_service = BlogService(blogs)

__all__ = [
    "user_service",
    "UserService",
    "navigation_service",
    "NavigationService",
    "project_service",
    "ProjectService",
    "blog_service",
    "BlogService",
]
