import os
import glob
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


# =========================
# СЕРВЕР ДЛЯ RENDER
# =========================

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
    
def get_material_files(prefix):
    files = glob.glob(f"{prefix}_*.*") 
    files.sort()
    return files


# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

MAIN_TEXT = (
    "📚 Добро пожаловать в Библиотеку Всезнайки!\n\n"
    "Здесь собраны материалы для учителей 0–4 классов: "
    "рабочие листы, игры, карточки, наглядности, "
    "интерактивные задания и многое другое.\n\n"
    "Выберите, что хотите сделать ↓"
)


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📚 Библиотека",
                callback_data="library"
            )
        ],
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
        [
            InlineKeyboardButton(
                "❤️ Моя библиотека",
                callback_data="my_library"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Помощь",
                callback_data="help"
            )
        ],
    ])


# =========================
# МЕНЮ БИБЛИОТЕКИ
# =========================

def library_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎓 0 класс",
                callback_data="grade_0"
            )
        ],
        [
            InlineKeyboardButton(
                "1️⃣ 1 класс",
                callback_data="grade_1"
            )
        ],
        [
            InlineKeyboardButton(
                "2️⃣ 2 класс",
                callback_data="grade_2"
            )
        ],
        [
            InlineKeyboardButton(
                "3️⃣ 3 класс",
                callback_data="grade_3"
            )
        ],
        [
            InlineKeyboardButton(
                "4️⃣ 4 класс",
                callback_data="grade_4"
            )
        ],
        [
            InlineKeyboardButton(
                "🧩 Универсальные материалы",
                callback_data="universal"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="back_main"
            )
        ],
    ])


# =========================
# МЕНЮ 0 КЛАССА
# =========================

def grade_zero_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔤 Обучение грамоте",
                callback_data="g0_literacy"
            )
        ],
        [
            InlineKeyboardButton(
                "🔢 Математика",
                callback_data="g0_math"
            )
        ],
        [
            InlineKeyboardButton(
                "🌍 Окружающий мир",
                callback_data="g0_world"
            )
        ],
        [
            InlineKeyboardButton(
                "✂️ Творчество и аппликации",
                callback_data="g0_creativity"
            )
        ],
        [
            InlineKeyboardButton(
                "🎮 Игры и интерактивы",
                callback_data="g0_games"
            )
        ],
        [
            InlineKeyboardButton(
                "🖼 Наглядные материалы",
                callback_data="g0_visuals"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 Рабочие листы",
                callback_data="g0_worksheets"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Назад к классам",
                callback_data="library"
            )
        ],
    ])


# =========================
# /START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        MAIN_TEXT,
        reply_markup=main_keyboard()
    )


# =========================
# ОБРАБОТКА КНОПОК
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    # Главное меню -> Библиотека
    if query.data == "library":
        await query.edit_message_text(
            "📚 Библиотека материалов\n\n"
            "Выберите раздел ↓",
            reply_markup=library_keyboard()
        )

    # Библиотека -> 0 класс
    elif query.data == "grade_0":
        await query.edit_message_text(
            "🎓 0 класс\n\n"
            "Выберите предмет или тип материала ↓",
            reply_markup=grade_zero_keyboard()
        )

         # 0 класс -> Обучение грамоте
    elif query.data == "g0_literacy":
        await query.edit_message_text(
            "🔤 Обучение грамоте\n\n"
            "Выберите раздел ↓",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔤 Буквы и звуки", callback_data="literacy_letters")],
                [InlineKeyboardButton("✍️ Прописи", callback_data="literacy_writing")],
                [InlineKeyboardButton("🧩 Игры и задания", callback_data="literacy_games")],
                [InlineKeyboardButton("📋 Рабочие листы", callback_data="literacy_worksheets")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="grade_0")]
            ])
        )
    elif query.data == "literacy_letters":
        await query.edit_message_text(
            "🔤 Буквы и звуки\n\n"
            "Выберите букву ↓",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("А", callback_data="letter_a")],
                [InlineKeyboardButton("О", callback_data="letter_o")],
                [InlineKeyboardButton("У", callback_data="letter_u")],
                [InlineKeyboardButton("И", callback_data="letter_i")],
                [InlineKeyboardButton("Э", callback_data="letter_e")],
                [InlineKeyboardButton("М", callback_data="letter_m")],
                [InlineKeyboardButton("Ы", callback_data="letter_y")],
                [InlineKeyboardButton("П", callback_data="letter_p")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="g0_literacy")]
            ])
    )
    elif query.data == "letter_a":
        await query.edit_message_text(
            "🔤 Буква А\n\n"
            "Выберите материал ↓",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✍️ Прописи", callback_data="letter_a_writing")],
                [InlineKeyboardButton("✂️ Аппликации", callback_data="letter_a_crafts")],
                [InlineKeyboardButton("🎮 Игры и задания", callback_data="letter_a_games")],
                [InlineKeyboardButton("📋 Рабочие листы", callback_data="letter_a_worksheets")],
                [InlineKeyboardButton("⬅️ Назад к буквам", callback_data="literacy_letters")]
            ])
    )
    elif query.data == "letter_a_writing":
        await query.edit_message_text(
            "✍️ Прописи — буква А\n\n"
            "Выберите материал ↓",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📄 Пропись №1", callback_data="a_writing_1")],
                [InlineKeyboardButton("📄 Пропись №2", callback_data="a_writing_2")],
                [InlineKeyboardButton("📄 Пропись №3", callback_data="a_writing_3")],
                [InlineKeyboardButton("⬅️ Назад к букве А", callback_data="letter_a")]
            ])
    )
    elif query.data == "back_main":
        await query.edit_message_text(
            MAIN_TEXT,
    reply_markup=main_keyboard()
        )


# =========================
# ЗАПУСК БОТА
# =========================

def main():
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
