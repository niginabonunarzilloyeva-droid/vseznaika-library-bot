import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def run_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Библиотека", callback_data="library")],
        [
            InlineKeyboardButton("🔎 Найти материал", callback_data="search"),
            InlineKeyboardButton("🤖 Спросить Всезнайку", callback_data="ai"),
        ],
        [
            InlineKeyboardButton("🎁 Бесплатные материалы", callback_data="free"),
            InlineKeyboardButton("⭐ Новинки", callback_data="new"),
        ],
        [InlineKeyboardButton("❤️ Моя библиотека", callback_data="my_library")],
        [InlineKeyboardButton("💬 Помощь", callback_data="help")],
    ]

    text = (
        "📚 Добро пожаловать в Библиотеку Всезнайки!\n\n"
        "Здесь собраны материалы для учителей 0–4 классов: "
        "рабочие листы, игры, карточки, наглядности, "
        "интерактивные задания и многое другое.\n\n"
        "Выберите, что хотите сделать ↓"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    # Render Web Service требует открытый HTTP-порт.
    # Сервер работает отдельно и не мешает Telegram-боту.
    threading.Thread(
        target=run_health_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
