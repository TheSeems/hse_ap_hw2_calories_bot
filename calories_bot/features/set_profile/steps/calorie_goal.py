from typing import Any, Dict

from dependency_injector.wiring import inject, Provide
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import CALORIE_GOAL
from calories_bot.features.third_party.weather.utils import get_temperature
from calories_bot.storage.profile import ProfileStorage

calorie_keyboard = ReplyKeyboardMarkup.from_row(
    ["1500", "2000", "2500", "Нет"],
    one_time_keyboard=True,
)


@inject
async def communicate_calorie_goal(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    if not update.message:
        return CALORIE_GOAL

    async def reply_try_again():
        await update.message.reply_text(
            "Отправьте, пожалуйста, количество калорий или 'нет'",
            reply_markup=calorie_keyboard,
        )
        return CALORIE_GOAL

    if not update.message.text:
        return await reply_try_again()

    profile = await profile_storage.load_profile(update.message.from_user.id)

    if update.message.text.lower() == "нет" or update.message.text.lower() == "no":
        calorie_goal = profile.get_default_calorie_goal()
    else:
        if not update.message.text.isnumeric():
            return await reply_try_again()
        calorie_goal = int(update.message.text)

    water_goal = profile.get_default_water_goal(
        temperature=await get_temperature(profile.lat, profile.lon)
    )

    profile.calorie_goal = calorie_goal
    profile.water_goal = water_goal
    profile.burned_calories = 0
    profile.logged_water = 0
    profile.active = True

    await profile_storage.save_profile(profile)
    await update.message.reply_text("Прекрасно! Ваш профиль заполнен")

    return ConversationHandler.END


def add_calorie_goal(states: Dict[int, Any]):
    states.update({
        CALORIE_GOAL: [MessageHandler(filters.Text(), communicate_calorie_goal)]
    })
