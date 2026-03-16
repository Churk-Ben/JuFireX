from datetime import datetime
import json

from backend.data.database import db


class VerificationTotp(db.Model):
    __tablename__ = "verification_totp"
    __bind_key__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, index=True)
    encrypted_totp_secret = db.Column(db.LargeBinary, nullable=False)
    recovery_codes = db.Column(db.Text, nullable=True)  # Stored as JSON string (hashed)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(
        self, uuid, encrypted_totp_secret, recovery_codes=None, is_active=False
    ):
        self.uuid = uuid
        self.encrypted_totp_secret = encrypted_totp_secret
        self.is_active = is_active
        if recovery_codes is not None:
            self.set_recovery_codes(recovery_codes)

    def set_recovery_codes(self, codes_list):
        self.recovery_codes = json.dumps(codes_list)

    def get_recovery_codes(self):
        if self.recovery_codes:
            return json.loads(self.recovery_codes)
        return []
