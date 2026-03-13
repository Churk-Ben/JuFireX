from datetime import datetime, timedelta

from backend.data.database import db


class VerificationCode(db.Model):
    __tablename__ = "verification_code"
    __bind_key__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False, index=True)
    code = db.Column(db.String(6), nullable=False)
    method = db.Column(db.String(20), nullable=False, default="email")
    scene = db.Column(db.String(20), nullable=False, default="register")
    created_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        identifier,
        code,
        method="email",
        scene="register",
        expires_in_minutes=15,
    ):
        self.identifier = identifier
        self.code = code
        self.method = method
        self.scene = scene
        self.expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)

    def is_valid(self):
        return not self.is_used and datetime.now() < self.expires_at
