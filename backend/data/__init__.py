from .repositories.user_repo import UserRepository
from .repositories.navigation_repo import NavigationRepository
from .repositories.project_repo import ProjectRepository
from .repositories.blog_repo import BlogRepository


users = UserRepository()
navigations = NavigationRepository()
projects = ProjectRepository()
blogs = BlogRepository()


__all__ = [
    "users",
    "UserRepository",
    "navigations",
    "NavigationRepository",
    "projects",
    "ProjectRepository",
    "blogs",
    "BlogRepository",
]
