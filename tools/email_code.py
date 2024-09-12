from flask_mail import Mail, Message
from config import app

mail = Mail(app)
def send_verification_email(email, v_code):
    subject = "请验证您的邮箱"
    sender = app.config['MAIL_USERNAME']
    recipients = [email]
    body = f"您的验证码是：{v_code}"
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = body
    mail.send(message)