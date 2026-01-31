from datetime import datetime
import uuid

from backend.data.database import db


def _get_uuid() -> str:
    return str(uuid.uuid4())


class Navigation(db.Model):
    __tablename__ = "navigation"
    __bind_key__ = "navigations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=_get_uuid)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(255), nullable=True, default="fas:link")
    description = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=True, default="default")
    owner_uuid = db.Column(db.String(36), nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "url": self.url,
            "icon": self.icon,
            "description": self.description,
            "category": self.category,
            "is_public": self.is_public,
            "order": self.order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Navigation {self.title}>"
