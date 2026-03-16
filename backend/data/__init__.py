from .repositories.user_repo import UserRepository
from .repositories.navigation_repo import NavigationRepository
from .repositories.project_repo import ProjectRepository
from .repositories.blog_repo import BlogRepository
from .repositories.verification_code_repo import VerificationCodeRepo


users = UserRepository()
navigations = NavigationRepository()
projects = ProjectRepository()
blogs = BlogRepository()
verifications = VerificationCodeRepo()


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
    "VerificationCodeRepo",
]
