from typing import List, Optional
from backend.data.models.nav import NavCategory, NavItem
from .db_repo import DBRepository


class NavCategoryRepository(DBRepository[NavCategory]):
    def __init__(self):
        super().__init__(NavCategory)

    def get_all_with_items(self) -> List[NavCategory]:
        # order by order field
        return NavCategory.query.order_by(NavCategory.order).all()


class NavItemRepository(DBRepository[NavItem]):
    def __init__(self):
        super().__init__(NavItem)
    
    def get_by_category(self, category_id: int) -> List[NavItem]:
        return NavItem.query.filter_by(category_id=category_id).order_by(NavItem.order).all()
