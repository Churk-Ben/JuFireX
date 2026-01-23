from typing import Optional, List
from backend.data.database import db
from backend.data.models.user import User, HiddenNavItem
from .db_repo import DBRepository


class UserRepository(DBRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def get_count(self) -> int:
        return self.count()

    # Hidden Nav Items logic remains specific to User domain
    def get_hidden_nav_items(self, user_id: int) -> List[int]:
        hidden_items = HiddenNavItem.query.filter_by(user_id=user_id).all()
        return [item.nav_item_id for item in hidden_items]

    def hide_nav_item(self, user_id: int, nav_item_id: int):
        existing = HiddenNavItem.query.filter_by(
            user_id=user_id, nav_item_id=nav_item_id
        ).first()
        if not existing:
            item = HiddenNavItem(user_id=user_id, nav_item_id=nav_item_id)
            db.session.add(item)
            db.session.commit()

    def unhide_nav_item(self, user_id: int, nav_item_id: int):
        existing = HiddenNavItem.query.filter_by(
            user_id=user_id, nav_item_id=nav_item_id
        ).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
