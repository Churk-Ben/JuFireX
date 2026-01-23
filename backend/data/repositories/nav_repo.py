from typing import List, Optional
from backend.data.database import db
from backend.data.models.nav import NavCategory, NavItem

class NavRepository:
    @staticmethod
    def get_categories() -> List[NavCategory]:
        return NavCategory.query.order_by(NavCategory.order).all()

    @staticmethod
    def get_category_by_id(cat_id: int) -> Optional[NavCategory]:
        return db.session.get(NavCategory, cat_id)

    @staticmethod
    def create_category(category: NavCategory) -> NavCategory:
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def update_category(category: NavCategory) -> NavCategory:
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category: NavCategory):
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[NavItem]:
        return db.session.get(NavItem, item_id)

    @staticmethod
    def create_item(item: NavItem) -> NavItem:
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update_item(item: NavItem) -> NavItem:
        db.session.commit()
        return item

    @staticmethod
    def delete_item(item: NavItem):
        db.session.delete(item)
        db.session.commit()
