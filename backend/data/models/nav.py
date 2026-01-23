from datetime import datetime

from backend.data.database import db

class NavCategory(db.Model):
    __bind_key__ = "navs"
    __tablename__ = "nav_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), default="fas fa-link")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    created_by_id = db.Column(db.Integer) # Logic link to User.id

    # Relationship to items
    nav_items = db.relationship(
        "NavItem", backref="category", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "order": self.order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by_id": self.created_by_id,
            "items": [item.to_dict() for item in self.nav_items]
        }

class NavItem(db.Model):
    __bind_key__ = "navs"
    __tablename__ = "nav_item"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default="fas fa-link")
    is_public = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    category_id = db.Column(db.Integer, db.ForeignKey("nav_category.id"))
    created_by_id = db.Column(db.Integer) # Logic link to User.id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "icon": self.icon,
            "is_public": self.is_public,
            "order": self.order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "category_id": self.category_id,
            "created_by_id": self.created_by_id
        }
