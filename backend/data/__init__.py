from .repositories.user_repo import UserRepository
from .repositories.navigation_repo import NavigationRepository
from .repositories.project_repo import ProjectRepository
from .repositories.blog_repo import BlogRepository
from .repositories.verification_repo import VerificationRepo


users = UserRepository()
navigations = NavigationRepository()
projects = ProjectRepository()
blogs = BlogRepository()
verifications = VerificationRepo()


__all__ = [
    "users",
    "UserRepository",
    "navigations",
    "NavigationRepository",
    "projects",
    "ProjectRepository",
    "blogs",
    "BlogRepository",
    "verifications",
    "VerificationRepo",
]
