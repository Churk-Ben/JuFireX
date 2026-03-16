# ------------------------------------------------------------
# @author: Churk
# @status: 已审查
# @description: 验证码服务层, 包含验证码发送, 验证等业务逻辑
# ------------------------------------------------------------

import random
import string
from typing import Tuple

from cryptography.fernet import Fernet
import pyotp

from backend.data import VerificationCodeRepo
from backend.config import Config
from backend.services import MailService


class VerificationService:
    def __init__(
        self, verification_repo: VerificationCodeRepo, mail_service: MailService
    ):
        self.repo = verification_repo
        self.mail_service = mail_service

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
            self.repo.add(identifier, code, method, scene)
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
            vc = self.repo.get_valid_code(identifier, code, method, scene)
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
        vc = self.repo.get_valid_code(identifier, code, method, scene)
        if vc:
            self.repo.mark_as_used(vc)
            return True
        return False

    def _send_email_code(self, email: str, code: str, scene: str) -> Tuple[bool, str]:
        """发送邮件验证码"""
        if not self.mail_service:
            return False, "邮件服务未配置"

        return self.mail_service.send_verification_code(scene, email, code)
