import os
from flask import Flask, request, jsonify
from telegram import Bot, Update
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # izinkan frontend fetch dari domain manapun

# Masukkan token bot langsung atau dari env variable
TOKEN = os.getenv("BOT_TOKEN") or "7411297347:AAGfiR6tVSY8vMNmI62UK_GA6fgvxEYLC9g"
bot = Bot(token=TOKEN)

# Variabel global untuk menyimpan pesan terbaru
latest_text = "Belum ada pesan masuk."
latest_from = None
latest_updated_at = None

@app.route('/')
def index():
    return f"<h1>Pesan Terbaru:</h1><p>{latest_text}</p>"

# Endpoint webhook Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    global latest_text, latest_from, latest_updated_at
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message and update.message.text:
        latest_text = update.message.text
        sender = update.message.from_user
        latest_from = f"{sender.first_name} {sender.last_name or ''}".strip() or sender.username
        latest_updated_at = datetime.utcnow().isoformat()

    return "ok", 200

# Endpoint untuk frontend fetch
@app.route('/latest')
def latest():
    return jsonify({
        "text": latest_text,
        "from": latest_from,
        "updated_at": latest_updated_at
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
