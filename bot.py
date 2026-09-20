import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


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
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
