import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Bot, Update
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# Token bot
TOKEN = "7411297347:AAGfiR6tVSY8vMNmI62UK_GA6fgvxEYLC9g"
bot = Bot(token=TOKEN)

# Simpan pesan terakhir (maks 50)
MESSAGES = []
MAX_MESSAGES = 50

def now_iso():
    return datetime.now(timezone.utc).isoformat()

@app.route('/')
def index():
    return "<h1>Backend Telegram History Running!</h1>"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if update.message and update.message.text:
        sender = update.message.from_user
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip() or sender.username or str(sender.id)
        MESSAGES.append({
            "text": update.message.text,
            "from": sender_name,
            "timestamp": now_iso()
        })
        # Keep only last MAX_MESSAGES
        if len(MESSAGES) > MAX_MESSAGES:
            MESSAGES.pop(0)
    return "ok", 200

@app.route("/latest")
def latest():
    return jsonify(MESSAGES)

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
