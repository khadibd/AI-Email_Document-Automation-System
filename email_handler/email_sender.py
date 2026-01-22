import smtplib
import logging
from email.message import EmailMessage
from config import SMTP_HOST, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD


class EmailSender:
    def send_reply(self, to_email, subject, body):
        try:
            msg = EmailMessage()
            msg["From"] = EMAIL_USER
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)

            logging.info(f"Reply sent to {to_email}")

        except Exception as e:
            logging.error(f"Failed to send reply to {to_email}: {e}")
