# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 邮件服务层, 包含邮件发送, 验证码发送等业务逻辑
# ------------------------------------------------------------

from flask import render_template
import resend

from backend.config import Config
from backend.core.Logger import get_logger

logger = get_logger("Service_Mail")


class MailService:
    def __init__(self):
        self.api_key = Config.RESEND_API_KEY
        if not self.api_key:
            logger.warning("未配置 Resend API Key")
        resend.api_key = self.api_key
        self.sender = Config.SENDER_EMAIL

    def send_email(self, to_email: str, subject: str, html_content: str):
        if not self.api_key:
            logger.error("未配置 Resend API Key, 无法发送邮件")
            return False, "邮件服务未配置"

        try:
            params = {
                "from": f"JuFireX Support <{self.sender}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }
            email = resend.Emails.send(params)
            logger.info(f"Email sent to {to_email}, ID: {email.get('id')}")
            return True, "邮件发送成功"
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False, f"邮件发送失败: {str(e)}"

    def send_verification_code(self, scene: str, to_email: str, code: str):
        subject_map = {
            "register": "JuFireX 注册验证码",
            "login": "JuFireX 登录验证码",
            "update_password": "JuFireX 修改密码验证码",
            "reset_password": "JuFireX 重置密码验证码",
            "bind_2fa": "JuFireX 绑定验证",
        }

        subject = subject_map.get(scene, "JuFireX 验证码")
        try:
            html = render_template(
                "emails/verification_code.html", subject=subject, code=code
            )
        except Exception as e:
            logger.error(f"Failed to render email template: {str(e)}")
            return False, f"邮件模板渲染失败: {str(e)}"

        return self.send_email(to_email, subject, html)

    # TODO: 警告邮件
    def send_warning_email(self, to_email: str, warning_message: str):
        subject = "JuFireX 警告通知"
        try:
            html = render_template("emails/warning.html", message=warning_message)
        except Exception as e:
            logger.error(f"Failed to render warning email template: {str(e)}")
            return False, f"警告邮件模板渲染失败: {str(e)}"

        return self.send_email(to_email, subject, html)
