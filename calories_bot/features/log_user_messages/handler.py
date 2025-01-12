import logging

from dependency_injector.wiring import inject
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


@inject
async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        logging.info(f"Получено сообщение: {update.message.text}")


handler = MessageHandler(filters.Text(), log_message, block=False)
