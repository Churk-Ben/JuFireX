from typing import Optional, List
from sqlalchemy import select
from backend.data.database import db
from backend.data.models.user import User
from backend.data.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(self.model).filter_by(username=username)
        return db.session.scalars(stmt).first()

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(self.model).filter_by(email=email)
        return db.session.scalars(stmt).first()

    def get_by_uuid(self, uuid: str) -> Optional[User]:
        stmt = select(self.model).filter_by(uuid=uuid)
        return db.session.scalars(stmt).first()

    def get_count(self) -> int:
        return self.model.query.count()
