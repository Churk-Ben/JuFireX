import os
from pathlib import Path

from dotenv import load_dotenv

# 一级目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DATABASE_DIR = PROJECT_ROOT / "database"
DEFAULTS_DIR = PROJECT_ROOT / "defaults"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
LOG_DIR = PROJECT_ROOT / "logs"

# 加载环境变量
load_dotenv(PROJECT_ROOT / ".env")

# 用户角色
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

    # 一级目录
    PROJECT_ROOT = PROJECT_ROOT
    BACKEND_DIR = BACKEND_DIR
    DATABASE_DIR = DATABASE_DIR
    DEFAULTS_DIR = DEFAULTS_DIR
    FRONTEND_DIR = FRONTEND_DIR
    LOG_DIR = LOG_DIR

    # 数据仓库及数据库路径
    PROFILES_DIR = DATABASE_DIR / "profiles"
    PROJECTS_DIR = DATABASE_DIR / "projects"
    NAVIGATIONS_DIR = DATABASE_DIR / "navigations"
    BLOGS_DIR = DATABASE_DIR / "blogs"

    PROFILES_DB_PATH = PROFILES_DIR / "users.db"
    NAVIGATIONS_DB_PATH = NAVIGATIONS_DIR / "navigations.db"

    # 日志配置
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")

    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{PROFILES_DB_PATH}"
    SQLALCHEMY_BINDS = {
        "users": f"sqlite:///{PROFILES_DB_PATH}",
        "navigations": f"sqlite:///{NAVIGATIONS_DB_PATH}",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def ensure_dirs():
        os.makedirs(Config.PROJECTS_DIR, exist_ok=True)
        os.makedirs(Config.PROFILES_DIR, exist_ok=True)
        os.makedirs(Config.NAVIGATIONS_DIR, exist_ok=True)
        os.makedirs(Config.BLOGS_DIR, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)


if __name__ == "__main__":
    Config.ensure_dirs()
