from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.storage.profile import ProfileStorage


@inject
async def log_water(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
):
    if not update.message:
        return
    if (await profile_storage.get_active_profile(update.message.from_user.id)) is None:
        await update.message.reply_text("Сначала заполните профиль: /set_profile")
        return
    if len(context.args) == 0 or not context.args[0].isnumeric():
        await update.message.reply_text("Введите количество выпитой воды в милилитрах")
        return
    volume = float(context.args[0])
    async with profile_storage.mutate_active_profile(update.message.from_user.id) as profile:
        profile.logged_water += volume
        await update.message.reply_text(
            f"Выпито +{round(volume)} мл. воды. "
            f"Прогресс: {round(profile.logged_water)} / {round(profile.water_goal)}"
        )


handler = CommandHandler("log_water", log_water)
