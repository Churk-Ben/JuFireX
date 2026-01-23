from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.data.database import db
from backend.config import ROLE_NAMES

class User(db.Model):
    __tablename__ = "user"
    __bind_key__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=0)  # ROLE_GUEST
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    avatar_path = db.Column(db.String(200), default=None)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "role_name": self.get_role_name(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
            "avatar_path": self.avatar_path
        }

    def get_role_name(self):
        return ROLE_NAMES.get(self.role, "未知")

    def __repr__(self):
        return f"<User {self.username}>"

class HiddenNavItem(db.Model):
    __tablename__ = "hidden_nav_item"
    __bind_key__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    nav_item_id = db.Column(db.Integer) # Logic link to NavItem.id (in navs.db)
    hidden_at = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship("User", backref=db.backref("hidden_nav_items", lazy=True))
