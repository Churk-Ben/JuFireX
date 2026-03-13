# ------------------------------------------------------------
# @author: Churk
# @status: 待审查
# @description: 邮件服务层, 包含邮件发送, 验证码发送等业务逻辑
# ------------------------------------------------------------

import resend

from backend.config import Config
from backend.core.Logger import get_logger

logger = get_logger("MailService")


class MailService:
    def __init__(self):
        self.api_key = Config.RESEND_API_KEY
        if not self.api_key:
            logger.warning("Resend API Key not found!")
        resend.api_key = self.api_key
        # TODO: 从配置中读取发件人
        self.sender = Config.SENDER_EMAIL

    def send_email(self, to_email: str, subject: str, html_content: str):
        if not self.api_key:
            logger.error("Cannot send email: API Key missing")
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

    def send_verification_code(self, to_email: str, code: str):
        subject = "JuFireX 邮箱验证码"
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #333;">欢迎注册 JuFireX</h2>
            <p>您的验证码是：</p>
            <div style="background-color: #f5f5f5; padding: 10px; text-align: center; border-radius: 4px;">
                <h1 style="color: #4CAF50; letter-spacing: 5px; margin: 0;">{code}</h1>
            </div>
            <p style="color: #666; font-size: 12px; margin-top: 20px;">该验证码将在 15 分钟后失效。</p>
            <p style="color: #666; font-size: 12px;">如果这不是您的操作，请忽略此邮件。</p>
        </div>
        """
        return self.send_email(to_email, subject, html)


if __name__ == "__main__":
    mail_service = MailService()
    mail_service.send_verification_code("2779675416@qq.com", "123456")
