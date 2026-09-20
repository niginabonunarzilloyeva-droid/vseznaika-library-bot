import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


# ---------- Сервер для Render ----------

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def run_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# ---------- Главное меню ----------

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📚 Библиотека",
            callback_data="library"
        )],

        [
            InlineKeyboardButton(
                "🔎 Найти материал",
                callback_data="search"
            ),
            InlineKeyboardButton(
                "🤖 Спросить Всезнайку",
                callback_data="ai"
            ),
        ],

        [
            InlineKeyboardButton(
                "🎁 Бесплатные материалы",
                callback_data="free"
            ),
            InlineKeyboardButton(
                "⭐ Новинки",
                callback_data="new"
            ),
        ],

        [InlineKeyboardButton(
            "❤️ Моя библиотека",
            callback_data="my_library"
        )],

        [InlineKeyboardButton(
            "💬 Помощь",
            callback_data="help"
        )],
    ])


MAIN_TEXT = (
    "📚 Добро пожаловать в Библиотеку Всезнайки!\n\n"
    "Здесь собраны материалы для учителей 0–4 классов: "
    "рабочие листы, игры, карточки, наглядности, "
    "интерактивные задания и многое другое.\n\n"
    "Выберите, что хотите сделать ↓"
)


# ---------- Команда /start ----------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        MAIN_TEXT,
        reply_markup=main_keyboard()
    )


# ---------- Обработка кнопок ----------

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    # Библиотека
    if query.data == "library":

        keyboard = [
            [InlineKeyboardButton(
                "🎓 0 класс",
                callback_data="grade_0"
            )],

            [InlineKeyboardButton(
                "1️⃣ 1 класс",
                callback_data="grade_1"
            )],

            [InlineKeyboardButton(
                "2️⃣ 2 класс",
                callback_data="grade_2"
            )],

            [InlineKeyboardButton(
                "3️⃣ 3 класс",
                callback_data="grade_3"
            )],

            [InlineKeyboardButton(
                "4️⃣ 4 класс",
                callback_data="grade_4"
            )],

            [InlineKeyboardButton(
                "🧩 Универсальные материалы",
                callback_data="universal"
            )],

            [InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="back_main"
            )],
        ]

        await query.edit_message_text(
            "📚 Библиотека материалов\n\n"
            "Выберите раздел ↓",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Возврат в главное меню
    elif query.data == "back_main":

        await query.edit_message_text(
            MAIN_TEXT,
            reply_markup=main_keyboard()
        )


# ---------- Запуск ----------

def main():

    # Render Web Service должен видеть открытый порт
    threading.Thread(
        target=run_health_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
