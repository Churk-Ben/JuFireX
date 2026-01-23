from datetime import datetime
import uuid

from werkzeug.security import check_password_hash, generate_password_hash

from backend.config import ROLE_NAMES
from backend.data.database import db


def _get_uuid() -> str:
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = "user"
    __bind_key__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=_get_uuid)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "role_name": self.get_role_name(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
        }

    def get_role_name(self):
        return ROLE_NAMES.get(self.role, "未知")

    def __repr__(self):
        return f"<User {self.username}>"
