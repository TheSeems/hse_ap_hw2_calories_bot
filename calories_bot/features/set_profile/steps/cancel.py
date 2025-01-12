from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import WEIGHT, HEIGHT
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_cancel(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    if not update.message:
        return ConversationHandler.END
    user_id = update.message.from_user.id
    await profile_storage.save_profile(Profile(user_id=user_id))
    await update.message.reply_text("Ваш профиль был сброшен")
    return ConversationHandler.END


cancel_handler = CommandHandler("cancel", communicate_cancel)
