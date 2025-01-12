from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from calories_bot.features.set_profile.states import WEIGHT


async def set_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Давайте начнем заполнять Ваш профиль. Начнем с веса. Укажите, пожалуйста, Ваш вес в кг."
    )
    return WEIGHT


command_handler = CommandHandler("set_profile", set_profile)
