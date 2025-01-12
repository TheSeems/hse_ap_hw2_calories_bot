from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.storage.profile import ProfileStorage

# Взято из головы - наобум
ACTIVITY_TO_CALORIE_COEFFICIENT = {
    "бег": ("🏃", 10),
    "плаванье": ("🏊", 8.5),
    "велосипед": ("🚴🏻", 7.5),
    "элипсоид": ("🔥", 6.5),
}


@inject
async def log_workout(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
):
    if not update.message:
        return
    if (await profile_storage.get_active_profile(update.message.from_user.id)) is None:
        await update.message.reply_text("Сначала заполните профиль: /set_profile")
        return

    async def send_usage():
        await update.message.reply_text("Используйте /log_workout <активность> <время (мин)>")

    if len(context.args) < 2:
        await send_usage()
        return

    activity = context.args[0]
    if activity not in ACTIVITY_TO_CALORIE_COEFFICIENT:
        await update.message.reply_text(
            f"Поддерживаемые виды активностей: {', '.join(ACTIVITY_TO_CALORIE_COEFFICIENT.keys())}")
        return

    minutes = context.args[1]
    if not minutes.isnumeric():
        await send_usage()
        return

    minutes = int(minutes)
    (icon, calorie_per_minute) = ACTIVITY_TO_CALORIE_COEFFICIENT[activity.lower()]
    additional_water = minutes / 30 * 200
    burned_calories = calorie_per_minute * minutes

    async with profile_storage.mutate_active_profile(update.message.from_user.id) as profile:
        profile.burned_calories += burned_calories
        profile.water_goal += additional_water

    await update.message.reply_text(
        f"{icon} {activity.title()} {minutes} мин. - {round(burned_calories)} ккал.\n"
        f"Дополнительно: выпейте {round(additional_water)} мл. воды.")


handler = CommandHandler("log_workout", log_workout)
