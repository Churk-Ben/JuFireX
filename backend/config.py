import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
DATABASE_DIR = PROJECT_ROOT / "database"

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# User Roles
ROLE_GUEST = 0
ROLE_MEMBER = 1
ROLE_ADMIN = 2
ROLE_SUPER_ADMIN = 3

ROLE_NAMES = {
    ROLE_GUEST: "游客",
    ROLE_MEMBER: "成员",
    ROLE_ADMIN: "管理员",
    ROLE_SUPER_ADMIN: "超级管理员",
}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "JuFireX-Secret-Key-Change-Me")
    
    # Data Paths
    PROFILES_DB_PATH = DATABASE_DIR / "profiles" / "users.db"
    NAVS_DB_PATH = DATABASE_DIR / "navs" / "navs.db"
    
    PROJECTS_DIR = DATABASE_DIR / "projects"
    BLOGS_DIR = DATABASE_DIR / "blogs"
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{PROFILES_DB_PATH}"
    SQLALCHEMY_BINDS = {
        "users": f"sqlite:///{PROFILES_DB_PATH}",
        "navs": f"sqlite:///{NAVS_DB_PATH}"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


    @staticmethod
    def ensure_dirs():
        os.makedirs(Config.PROJECTS_DIR, exist_ok=True)
        os.makedirs(Config.BLOGS_DIR, exist_ok=True)
        os.makedirs(Config.PROFILES_DB_PATH.parent, exist_ok=True)
        os.makedirs(Config.NAVS_DB_PATH.parent, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)
