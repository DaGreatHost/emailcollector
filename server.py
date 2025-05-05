from flask import Flask, request, render_template_string
import json, os

app = Flask(__name__)
PENDING_FILE = "pending.json"
VERIFIED_FILE = "verified.json"
EMAIL_LOG_FILE = "verified_emails.txt"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verification Success</title></head>
<body style="text-align:center;font-family:sans-serif;padding:40px;">
<h1>✅ Email Verified!</h1><p>You may now return to Telegram and type <b>/verified</b> to get your access link.</p>
</body></html>
"""

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

@app.route("/verify")
def verify():
    token = request.args.get("token")
    pending = load_json(PENDING_FILE)
    verified = load_json(VERIFIED_FILE)
    if token and token in pending:
        user_data = pending.pop(token)
        verified[user_data["user_id"]] = user_data["email"]
        save_json(PENDING_FILE, pending)
        save_json(VERIFIED_FILE, verified)
        telegram_username = user_data.get("username", "unknown")
        with open(EMAIL_LOG_FILE, "a") as f:
            f.write(f"{user_data['email']} | @{telegram_username}\n")
        return render_template_string(HTML_PAGE)
    return "Invalid or expired token", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
app.run(host="0.0.0.0", port=port)
