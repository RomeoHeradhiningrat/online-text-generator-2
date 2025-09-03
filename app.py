import os
from flask import Flask, request, jsonify
from telegram import Bot, Update

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
bot = Bot(token=TOKEN)

latest_text = "Belum ada pesan masuk."
latest_from = None
latest_time = None

@app.route("/")
def index():
    return f"<h1>Pesan Terbaru:</h1><p>{latest_text}</p><p>Dari: {latest_from}</p><p>Waktu: {latest_time}</p>"

@app.route(f"/webhook/<secret>", methods=["POST"])
def webhook(secret):
    global latest_text, latest_from, latest_time
    if secret != WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "wrong secret"}), 403

    update = Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.text:
        latest_text = update.message.text
        sender = update.message.from_user
        latest_from = f"{sender.first_name} {sender.last_name or ''}".strip()
        latest_time = update.message.date.isoformat()
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
