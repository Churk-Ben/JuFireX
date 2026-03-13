from backend.data import blogs, navigations, projects, users, verifications

from .blog_service import BlogService
from .mail_service import MailService
from .navigation_service import NavigationService
from .project_service import ProjectService
from .user_service import UserService
from .verification_service import VerificationService

mail_service = MailService()
verification_service = VerificationService(verifications, mail_service)
user_service = UserService(users, verifications)
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
    "mail_service",
    "MailService",
    "verification_service",
    "VerificationService",
]
