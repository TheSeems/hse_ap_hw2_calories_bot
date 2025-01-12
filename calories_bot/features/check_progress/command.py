from textwrap import dedent

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.storage.profile import ProfileStorage


@inject
async def check_progress(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
):
    if not update.message:
        return
    profile = await profile_storage.get_active_profile(update.message.from_user.id)
    if profile is None:
        await update.message.reply_text("Сначала заполните профиль: /set_profile")
        return
    await update.message.reply_text(dedent(f"""
        📊 Прогресс:
        Вода:
        - Выпито: {round(profile.logged_water)} мл из {round(profile.water_goal)} мл.
        - Осталось: {round(profile.water_goal) - round(profile.logged_water)} мл.
        
        Калории:
        - Потреблено: {round(profile.logged_calories)} ккал из {round(profile.calorie_goal)} ккал.
        - Сожжено: {round(profile.burned_calories)} ккал.
        - Баланс: {round(profile.logged_calories) - round(profile.burned_calories)} ккал.
        """))


handler = CommandHandler("check_progress", check_progress)
