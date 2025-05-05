from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from email_utils import send_verification_email
import secrets, json, os

print("🚀 Starting bot...")

TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = "https://t.me/+lmIxMokH59czZjg1"
PENDING_FILE = "pending.json"
VERIFIED_FILE = "verified.json"
EMAIL_LOG = "verified_emails.txt"

# Load/save functions
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Please send your email to continue:")

# Email handler
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    user_id = str(update.message.from_user.id)
    code = secrets.token_hex(3)

    pending = load_json(PENDING_FILE)
    pending[user_id] = {"email": email, "code": code}
    save_json(PENDING_FILE, pending)

    if send_verification_email(email, code):
        await update.message.reply_text("📧 Verification code sent! Reply with /code <your_code>")
    else:
        await update.message.reply_text("⚠️ Failed to send email. Please try again or contact admin.")

# Code handler
async def verify_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❌ Please provide your code. Example: /code 1a2b3c")
        return

    user_id = str(update.message.from_user.id)
    pending = load_json(PENDING_FILE)
    verified = load_json(VERIFIED_FILE)

    if user_id in pending and pending[user_id]["code"] == args[0]:
        email = pending[user_id]["email"]
        verified[user_id] = email
        save_json(VERIFIED_FILE, verified)

        # Append to email log
        with open(EMAIL_LOG, "a") as f:
            f.write(f"{update.message.from_user.username or user_id} | {email}\n")

        del pending[user_id]
        save_json(PENDING_FILE, pending)

        await update.message.reply_text(f"✅ Verified! Join the group: {GROUP_LINK}")
    else:
        await update.message.reply_text("❌ Invalid code or expired.")

# Main app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("code", verify_code))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))

if __name__ == "__main__":
    app.run_polling()
