# ------------------------------------------------------------
# @author: Churk
# @status: 待审查
# @description: 验证码服务层, 包含验证码发送, 验证等业务逻辑
# ------------------------------------------------------------

import random
import string
from typing import Tuple

from backend.data.repositories.verification_repo import VerificationRepo
from backend.services.mail_service import MailService


class VerificationService:
    def __init__(self, verification_repo: VerificationRepo, mail_service: MailService):
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
        # 获取有效验证码
        vc = self.repo.get_valid_code(identifier, code, method, scene)

        if not vc:
            return False, "验证码无效或已过期"

        return True, "验证码正确"

    def consume_code(
        self, identifier: str, code: str, method: str = "email", scene: str = "register"
    ) -> bool:
        """
        消耗验证码（标记为已使用）
        """
        vc = self.repo.get_valid_code(identifier, code, method, scene)
        if vc:
            self.repo.mark_as_used(vc)
            return True
        return False

    def _send_email_code(self, email: str, code: str, scene: str) -> Tuple[bool, str]:
        """发送邮件验证码"""
        if not self.mail_service:
            return False, "邮件服务未配置"

        subject_map = {
            "register": "JuFireX 注册验证码",
            "login": "JuFireX 登录验证码",
            "reset_password": "JuFireX 重置密码验证码",
            "bind_2fa": "JuFireX 绑定验证",
        }

        subject = subject_map.get(scene, "JuFireX 验证码")

        # 简单复用之前的 HTML 模板，后续可根据 scene 优化模板
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #333;">{subject}</h2>
            <p>您的验证码是：</p>
            <div style="background-color: #f5f5f5; padding: 10px; text-align: center; border-radius: 4px;">
                <h1 style="color: #4CAF50; letter-spacing: 5px; margin: 0;">{code}</h1>
            </div>
            <p style="color: #666; font-size: 12px; margin-top: 20px;">该验证码将在 15 分钟后失效。</p>
            <p style="color: #666; font-size: 12px;">如果这不是您的操作，请忽略此邮件。</p>
        </div>
        """

        return self.mail_service.send_email(email, subject, html)
