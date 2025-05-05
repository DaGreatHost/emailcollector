import smtplib
from email.mime.text import MIMEText
import os

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASS = os.getenv("SMTP_PASS")

def send_verification_email(to_email: str, code: str):
    subject = "🔐 Email Verification Code"
    body = f"""
    Hello!

    Your verification code is: {code}

    Please go back to Telegram and enter this code to verify your email.

    — TG Reward Bot
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SMTP_EMAIL, SMTP_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("❌ Email send error:", e)
        return False
