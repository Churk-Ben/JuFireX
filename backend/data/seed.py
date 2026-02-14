# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 数据库播种模块
# ------------------------------------------------------------

import json
from pathlib import Path
import random

from backend.config import Config, ROLE_SUPER_ADMIN
from backend.core.Logger import get_logger
from backend.data import navigations as nav_repo
from backend.data.database import db
from backend.data.models.navigation import Navigation
from backend.data.models.user import User


logger = get_logger("Seeder")


def seed_super_admin():
    """创建默认超级管理员账户"""
    CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

    super_admin = User(
        username=Config.SUPER_ADMIN_NAME,
        email=Config.SUPER_ADMIN_EMAIL,
        role=ROLE_SUPER_ADMIN,
        is_active=True,
    )

    # 生成随机密码
    init_password = "".join(random.choice(CHARSET) for _ in range(12))
    super_admin.set_password(init_password)
    db.session.add(super_admin)
    db.session.commit()

    # 创建用户文件夹
    user_folder: Path = Config.PROFILES_DIR / super_admin.uuid
    user_folder.mkdir(parents=True, exist_ok=True)

    # 在日志中记录播种信息
    msg = (
        "=" * 50
        + f"""
        创建默认超级管理员账户:
        - 用户名: {Config.SUPER_ADMIN_NAME}
        - 邮箱: {Config.SUPER_ADMIN_EMAIL}
        - 初始密码: {init_password}
        - UUID: {super_admin.uuid}
        
        请务必记录好初始密码! 后续登录后请及时修改密码!
        """
        + "=" * 50
    )
    logger.info(msg)

    # 在根目录生成密码文件
    with (Config.PROJECT_ROOT / "password.txt").open("w") as f:
        f.write("# format: uuid:password\n")
        f.write(f"{super_admin.uuid}:{init_password}")


def seed_navigations(navs: list):
    """播种默认导航项"""
    try:
        count = 0
        for item in navs:
            nav = Navigation(
                title=item["title"],
                url=item["url"],
                icon=item.get("icon", "fas:link"),
                description=item.get("description", ""),
                category=item.get("category", "default"),
                is_public=item.get("is_public", True),
                order=item.get("order", 0),
                owner_uuid=Config.OWNER_UUID,
            )
            db.session.add(nav)
            count += 1

        db.session.commit()
        nav_repo._sync_categories()

        logger.info(f"已播种 {count} 个默认导航项")

    except Exception as e:
        logger.error(f"播种导航项失败: {e}")
        db.session.rollback()


def seed():
    """数据库播种"""
    # 处理超级管理员
    if Config.KEEP_SUPER_ADMIN_EXIST:
        if not User.query.filter_by(role=ROLE_SUPER_ADMIN).first():
            seed_super_admin()

    # 处理导航项
    if Config.RESEED_DEFAULT_NAVIGATIONS:
        nav_file = Config.DEFAULTS_DIR / "navigation.json"
        flag_file = Config.DEFAULTS_DIR / "navigation.seeded"
        if not nav_file.exists():
            logger.warning(f"默认导航文件不存在: {nav_file}")
        elif flag_file.exists():
            logger.info(f"默认导航项已播种: {flag_file}")
        else:
            with nav_file.open("r", encoding="utf-8") as f:
                navs = json.load(f) or []
            seed_navigations(navs)
            # 创建标志文件 seeded 状态
            flag_file.touch()
