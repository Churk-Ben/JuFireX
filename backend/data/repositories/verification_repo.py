# ------------------------------------------------------------
# @author: Churk
# @status: 完工
# @description: 验证码数据仓库, 封装 VerificationCode 模型的所有数据库操作
# ------------------------------------------------------------

from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select

from backend.data.database import db
from backend.data.models.verification_code import VerificationCode


class VerificationRepo:
    def __init__(self):
        self.model = VerificationCode

    def add(
        self,
        identifier: str,
        code: str,
        method: str = "email",
        scene: str = "register",
        expires_in_minutes: int = 15,
    ) -> VerificationCode:
        # 清理同一标识符、同一场景下的旧验证码，防止堆积
        self.delete_previous_codes(identifier, method, scene)

        vc = VerificationCode(
            identifier=identifier,
            code=code,
            method=method,
            scene=scene,
            expires_in_minutes=expires_in_minutes,
        )
        db.session.add(vc)
        db.session.commit()
        return vc

    def get_valid_code(
        self,
        identifier: str,
        code: str,
        method: str,
        scene: str,
    ) -> Optional[VerificationCode]:
        """获取有效且未使用的验证码"""
        stmt = select(self.model).filter_by(
            identifier=identifier,
            code=code,
            method=method,
            scene=scene,
            is_used=False,
        )
        vc = db.session.scalars(stmt).first()
        if vc and vc.is_valid():
            return vc
        return None

    def mark_as_used(self, vc: VerificationCode):
        """标记验证码为已使用"""
        vc.is_used = True
        db.session.add(vc)
        db.session.commit()

    def delete_previous_codes(self, identifier: str, method: str, scene: str):
        """删除旧的验证码记录"""
        stmt = delete(self.model).where(
            self.model.identifier == identifier,
            self.model.method == method,
            self.model.scene == scene,
        )
        db.session.execute(stmt)
        db.session.commit()
