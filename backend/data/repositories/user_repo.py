from typing import Optional, List
from ..database import db
from ..models.user import User, HiddenNavItem


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        return user

    @staticmethod
    def delete(user: User):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_count() -> int:
        return User.query.count()

    # Hidden Nav Items
    @staticmethod
    def get_hidden_nav_items(user_id: int) -> List[int]:
        hidden_items = HiddenNavItem.query.filter_by(user_id=user_id).all()
        return [item.nav_item_id for item in hidden_items]

    @staticmethod
    def hide_nav_item(user_id: int, nav_item_id: int):
        existing = HiddenNavItem.query.filter_by(
            user_id=user_id, nav_item_id=nav_item_id
        ).first()
        if not existing:
            item = HiddenNavItem(user_id=user_id, nav_item_id=nav_item_id)
            db.session.add(item)
            db.session.commit()

    @staticmethod
    def unhide_nav_item(user_id: int, nav_item_id: int):
        existing = HiddenNavItem.query.filter_by(
            user_id=user_id, nav_item_id=nav_item_id
        ).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
