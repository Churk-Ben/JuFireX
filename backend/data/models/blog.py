from datetime import datetime
import uuid

from backend.data.database import db


def _get_uuid() -> str:
    return str(uuid.uuid4())


class Blog(db.Model):
    __tablename__ = "blog"
    __bind_key__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=_get_uuid)
    owner_uuid = db.Column(db.String(36), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "owner_uuid": self.owner_uuid,
            "is_public": self.is_public,
            "views": self.views,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
