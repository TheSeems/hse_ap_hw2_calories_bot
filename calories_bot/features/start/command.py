from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добрый день! Начните пользоваться ботом заполнив профиль: /set_profile"
    )


handler = CommandHandler("start", start)