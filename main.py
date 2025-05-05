from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from email_utils import send_verification_email
import secrets, json, os

TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = "https://t.me/+lmIxMokH59czZjg1"
PENDING_FILE = "pending.json"
VERIFIED_FILE = "verified.json"

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Please send your email to continue:")

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "unknown"
    token = secrets.token_urlsafe(16)
    pending = load_json(PENDING_FILE)
    pending[token] = {"email": email, "user_id": user_id, "username": username}
    save_json(PENDING_FILE, pending)
    send_verification_email(email, token)
    await update.message.reply_text("📧 A confirmation link has been sent to your email. Please check and click it.")

async def verified(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    verified = load_json(VERIFIED_FILE)
    if user_id in verified:
        await update.message.reply_text(f"✅ Already verified! Join here: {GROUP_LINK}")
    else:
        await update.message.reply_text("⏳ You're not verified yet. Please check your email.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verified", verified))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    app.run_polling()