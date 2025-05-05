import smtplib, ssl, os
from email.message import EmailMessage

SMTP_SERVER = "mail.tgreward.shop"
SMTP_PORT = 465
EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASS")

# Use the live Railway domain
RAILWAY_VERIFY_BASE = "https://web-production-86589.up.railway.app/verify?token="

def send_verification_email(to_email, token):
    confirm_link = f"{RAILWAY_VERIFY_BASE}{token}"
    msg = EmailMessage()
    msg['Subject'] = "Confirm your email for VIP Access"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f"Hi!\n\nClick this link to confirm your email:\n{confirm_link}\n\nOnce done, go back to the bot and type /verified.")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
