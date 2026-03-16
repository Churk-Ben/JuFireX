from backend.data.database import db
from backend.data.models.verification_totp import VerificationTotp


class VerificationTotpRepo:
    def get_by_uuid(self, uuid: str) -> VerificationTotp:
        return VerificationTotp.query.filter_by(uuid=uuid).first()

    def create_or_update(
        self, uuid: str, encrypted_totp_secret: bytes, recovery_codes: list = None
    ) -> VerificationTotp:
        totp_record = self.get_by_uuid(uuid)
        if totp_record:
            totp_record.encrypted_totp_secret = encrypted_totp_secret
            if recovery_codes is not None:
                totp_record.set_recovery_codes(recovery_codes)
        else:
            totp_record = VerificationTotp(
                uuid=uuid,
                encrypted_totp_secret=encrypted_totp_secret,
                recovery_codes=recovery_codes,
            )
            db.session.add(totp_record)

        db.session.commit()
        return totp_record

    def delete_by_uuid(self, uuid: str) -> bool:
        totp_record = self.get_by_uuid(uuid)
        if totp_record:
            db.session.delete(totp_record)
            db.session.commit()
            return True
        return False
