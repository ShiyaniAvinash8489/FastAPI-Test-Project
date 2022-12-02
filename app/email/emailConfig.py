# SMTP Server
import smtplib

# Email
from email.message import EmailMessage

# Settings
from app.config import settings


"""
****************************************************************************************
                                    Email Config
****************************************************************************************
"""


def send_email_verify_account_html(To, Subject, email_body):

    msg = EmailMessage()
    msg["Subject"] = Subject
    msg["From"] = settings.email_username
    msg["To"] = To
    msg.set_content(email_body)
    # msg["To"] = ", ".join(To)

    with smtplib.SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port) as smtp:
        smtp.login(settings.email_username, settings.email_password)
        smtp.send_message(msg=msg)

    return "ok"
