import os
from pathlib import Path

from dotenv import load_dotenv

# 重要目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DATABASE_DIR = PROJECT_ROOT / "database"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
LOG_DIR = PROJECT_ROOT / "logs"

DEFAULTS_DIR = DATABASE_DIR / "defaults"
BACKUP_ROOT = DATABASE_DIR / "backups"

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
    # 密钥配置
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "secretkey")
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "resendkey")
    TOTP_MASTER_KEY = os.environ.get("TOTP_MASTER_KEY", "totpkey")

    # 其他配置
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    SEED = os.environ.get("SEED", "false").lower() == "true"

    # 重要目录
    PROJECT_ROOT = PROJECT_ROOT
    BACKEND_DIR = BACKEND_DIR
    DATABASE_DIR = DATABASE_DIR
    FRONTEND_DIR = FRONTEND_DIR
    LOG_DIR = LOG_DIR

    DEFAULTS_DIR = DEFAULTS_DIR
    BACKUP_ROOT = BACKUP_ROOT

    # 数据仓库及数据库路径
    PROFILES_DIR = DATABASE_DIR / "profiles"
    PROJECTS_DIR = DATABASE_DIR / "projects"
    NAVIGATIONS_DIR = DATABASE_DIR / "navigations"
    BLOGS_DIR = DATABASE_DIR / "blogs"

    PROFILES_DB_PATH = PROFILES_DIR / "users.db"
    NAVIGATIONS_DB_PATH = NAVIGATIONS_DIR / "navigations.db"
    PROJECTS_DB_PATH = PROJECTS_DIR / "projects.db"
    BLOGS_DB_PATH = BLOGS_DIR / "blogs.db"

    # 版本信息
    VERSION_FILE = PROJECT_ROOT / "version"

    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{PROFILES_DB_PATH}"
    SQLALCHEMY_BINDS = {
        "users": f"sqlite:///{PROFILES_DB_PATH}",
        "navigations": f"sqlite:///{NAVIGATIONS_DB_PATH}",
        "projects": f"sqlite:///{PROJECTS_DB_PATH}",
        "blogs": f"sqlite:///{BLOGS_DB_PATH}",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 默认超级管理员播种配置
    KEEP_SUPER_ADMIN_EXIST = True
    SUPER_ADMIN_NAME = "System"
    SUPER_ADMIN_EMAIL = "admin@jufirex.com"

    # 默认导航项播种配置
    RESEED_DEFAULT_NAVIGATIONS = True
    OWNER_UUID = None

    # RESEND 配置
    SENDER_EMAIL = "noreply@support.jufirex.com"

    # TOTP 配置
    TOTP_WINDOW_TOLERANCE = 1

    @staticmethod
    def ensure_dirs():
        Config.PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        Config.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        Config.NAVIGATIONS_DIR.mkdir(parents=True, exist_ok=True)
        Config.BLOGS_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        Config.DEFAULTS_DIR.mkdir(parents=True, exist_ok=True)
        Config.BACKUP_ROOT.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    Config.ensure_dirs()
