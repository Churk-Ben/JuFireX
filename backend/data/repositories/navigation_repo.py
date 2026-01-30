# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航数据仓库, 封装 Navigation 模型的所有数据库操作
# ------------------------------------------------------------

import json
from typing import List, Optional

from sqlalchemy import distinct, or_, select

from backend.config import Config
from backend.core.Logger import get_logger
from backend.data.database import db
from backend.data.models.navigation import Navigation

logger = get_logger("Repo_Navigation")


class NavigationRepository:
    """
    导航数据仓库, 封装 Navigation 模型的所有数据库操作
    """

    def __init__(self):
        self.model = Navigation

    def _sync_categories(self):
        """同步分类到 JSON 文件"""
        try:
            # 获取所有非空分类
            stmt = select(distinct(self.model.category)).where(
                self.model.category.is_not(None)
            )
            categories = list(db.session.scalars(stmt).all())
            # 过滤掉可能的空字符串
            categories = [c for c in categories if c]

            file_path = Config.NAVIGATIONS_DIR / "categories.json"

            # 写入文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(categories, f, ensure_ascii=False, indent=2)

            logger.info(f"已同步分类: {categories}")
        except Exception as e:
            # 记录错误但不中断流程
            logger.error(f"同步分类到 JSON 文件时出错: {e}")

    def get_by_uuid(self, uuid: str) -> Optional[Navigation]:
        """根据 UUID 获取导航项"""
        stmt = select(self.model).filter_by(uuid=uuid)
        return db.session.scalars(stmt).first()

    def get_all(
        self, user_uuid: str = None, view_all: bool = False
    ) -> List[Navigation]:
        """
        获取导航列表.
        :param user_uuid: 当前用户 UUID
        :param view_all: 是否查看所有数据 (仅限管理员明确请求时)
        """
        stmt = select(self.model)

        if view_all:
            # 查看所有数据 (管理视图)
            pass
        elif user_uuid:
            # 登录用户: 公开 OR 自己的
            stmt = stmt.where(
                or_(self.model.is_public == True, self.model.owner_uuid == user_uuid)
            )
        else:
            # 游客: 仅公开
            stmt = stmt.filter_by(is_public=True)

        stmt = stmt.order_by(self.model.order.desc(), self.model.created_at.desc())
        return list(db.session.scalars(stmt).all())

    def add(self, data: dict) -> Navigation:
        """添加新的导航项"""
        nav = self.model(**data)
        db.session.add(nav)
        db.session.commit()
        self._sync_categories()
        return nav

    def update(self, uuid: str, data: dict) -> Optional[Navigation]:
        """更新导航项"""
        nav = self.get_by_uuid(uuid)
        if not nav:
            return None

        for key, value in data.items():
            if hasattr(nav, key):
                setattr(nav, key, value)

        db.session.commit()
        self._sync_categories()
        return nav

    def delete(self, uuid: str) -> bool:
        """删除导航项"""
        nav = self.get_by_uuid(uuid)
        if not nav:
            return False

        db.session.delete(nav)
        db.session.commit()
        self._sync_categories()
        return True
