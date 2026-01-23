from typing import Optional, List
from backend.data.database import db
from backend.data.models.user import User
from .db_repo import DBRepository


class UserRepository(DBRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> List[User]:
        return User.query.filter_by(username=username).all()

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def get_by_uuid(self, uuid: str) -> Optional[User]:
        return User.query.filter_by(uuid=uuid).first()

    def get_count(self) -> int:
        return self.count()
