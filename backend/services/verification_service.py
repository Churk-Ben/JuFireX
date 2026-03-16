# ------------------------------------------------------------
# @author: Churk
# @status: 已审查
# @description: 验证码服务层, 包含验证码发送, 验证等业务逻辑
# ------------------------------------------------------------

import random
import string
from typing import Tuple

from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

from backend.data import VerificationCodeRepo, VerificationTotpRepo
from backend.config import Config
from backend.services import MailService


class VerificationService:
    def __init__(
        self,
        mail_service: MailService,
        code_repo: VerificationCodeRepo,
        totp_repo: VerificationTotpRepo = None,
    ):
        self.mail_service = mail_service
        self.code_repo = code_repo
        self.totp_repo = totp_repo
        self.cipher = Fernet(Config.TOTP_MASTER_KEY.encode())

    def _send_email_code(self, email: str, code: str, scene: str) -> Tuple[bool, str]:
        """发送邮件验证码"""
        if not self.mail_service:
            return False, "邮件服务未配置"

        return self.mail_service.send_verification_code(scene, email, code)

    def _encrypt_secret(self, cipher: Fernet, plain_secret: str) -> bytes:
        """加密 TOTP Secret"""
        return cipher.encrypt(plain_secret.encode())

    def _decrypt_secret(self, cipher: Fernet, encrypted_secret: bytes) -> str:
        """解密 TOTP Secret"""
        return cipher.decrypt(encrypted_secret).decode()

    def send_code(
        self, identifier: str, method: str = "email", scene: str = "register"
    ) -> Tuple[bool, str]:
        """
        统一发送验证码逻辑
        """
        # 1. 生成验证码
        code = "".join(random.choices(string.digits, k=6))

        # 2. 保存到数据库
        try:
            self.code_repo.add(identifier, code, method, scene)
        except Exception as e:
            return False, f"验证码生成失败: {str(e)}"

        # 3. 根据 method 发送
        if method == "email":
            return self._send_email_code(identifier, code, scene)
        elif method == "sms":
            return False, "短信服务暂未实现"
        elif method == "totp":
            return False, "TOTP 不需要发送验证码"
        else:
            return False, "不支持的验证方式"

    def verify_code(
        self, identifier: str, code: str, method: str = "email", scene: str = "register"
    ) -> Tuple[bool, str]:
        """
        统一验证逻辑
        """
        if method == "email" or method == "sms":
            if method == "sms":
                return False, "短信服务暂未实现"

            # 获取有效邮箱验证码
            vc = self.code_repo.get_valid_code(identifier, code, method, scene)
            if not vc:
                return False, "验证码无效或已过期"
            return True, "验证码正确"

        elif method == "totp":
            # TODO: 实现 TOTP 验证逻辑
            return False, "TOTP 验证待实现"

        else:
            return False, "不支持的验证方式"

    def consume_code(
        self, identifier: str, code: str, method: str = "email", scene: str = "register"
    ) -> bool:
        """消耗验证码（标记为已使用）"""
        vc = self.code_repo.get_valid_code(identifier, code, method, scene)
        if vc:
            self.code_repo.mark_as_used(vc)
            return True
        return False

    def setup_totp(self, identifier: str) -> Tuple[bool, any]:
        """设置 TOTP 验证"""
        if not self.totp_repo:
            return False, "TOTP 存储未配置"

        raw_secret = pyotp.random_base32()
        provisioning_uri = pyotp.totp.TOTP(raw_secret).provisioning_uri(
            name=identifier, issuer_name="JuFireX"
        )
        encrypted_secret = self._encrypt_secret(self.cipher, raw_secret)

        # 尝试生成恢复代码
        recovery_codes = [
            "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            for _ in range(8)
        ]
        hashed_recovery_codes = [
            generate_password_hash(code) for code in recovery_codes
        ]

        try:
            self.totp_repo.create_or_update(
                uuid=identifier,
                encrypted_totp_secret=encrypted_secret,
                recovery_codes=hashed_recovery_codes,
            )
            return True, {"uri": provisioning_uri, "recovery_codes": recovery_codes}
        except Exception as e:
            return False, f"TOTP 设置失败: {str(e)}"

    def is_totp_enabled(self, identifier: str) -> bool:
        """检查用户是否启用了 TOTP 验证"""
        if not self.totp_repo:
            return False
        totp_record = self.totp_repo.get_by_uuid(identifier)
        return totp_record is not None and bool(totp_record.encrypted_totp_secret)

    def verify_totp(self, identifier: str, token: str) -> Tuple[bool, str]:
        """验证 TOTP 令牌"""
        if not self.totp_repo:
            return False, "TOTP 存储未配置"

        totp_record = self.totp_repo.get_by_uuid(identifier)
        if not totp_record or not totp_record.encrypted_totp_secret:
            return False, "未配置 TOTP 验证"

        secret = self._decrypt_secret(self.cipher, totp_record.encrypted_totp_secret)
        window_tolerance = Config.TOTP_WINDOW_TOLERANCE
        totp = pyotp.TOTP(secret)

        # 验证 TOTP code
        if totp.verify(token, valid_window=window_tolerance):
            return True, "TOTP 验证成功"

        # 尝试验证是否是恢复代码
        recovery_codes = totp_record.get_recovery_codes()
        for hashed_code in recovery_codes:
            if check_password_hash(hashed_code, token):
                # 恢复代码只能使用一次，使用后需要移除
                recovery_codes.remove(hashed_code)
                self.totp_repo.create_or_update(
                    uuid=identifier,
                    encrypted_totp_secret=totp_record.encrypted_totp_secret,
                    recovery_codes=recovery_codes,
                )
                return True, "恢复代码验证成功"

        return False, "TOTP 验证失败"
