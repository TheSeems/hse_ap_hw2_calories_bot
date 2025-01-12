from typing import Any, Dict

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import CITY, CALORIE_GOAL
from calories_bot.features.set_profile.steps.calorie_goal import calorie_keyboard
from calories_bot.features.third_party.weather.utils import get_location, get_temperature
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_city(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    if not update.message:
        return CITY
    city = update.message.text
    if not city:
        await update.message.reply_text("Отправьте, пожалуйста, название города где Вы находитесь")
    async with profile_storage.mutate_profile(update.message.from_user.id) as profile:
        location = get_location(city)
        profile.lat = location.lat
        profile.lon = location.lon
        profile.city = city
    await update.message.reply_text(
        f"Прекрасно! В {location.name} ({location.country}) сейчас "
        f"{await get_temperature(location.lat, location.lon)} °C. "
        "Если хотите указать цель по калориям, напишите её в новом сообщении (или выберете из готовых). "
        "Иначе напишите 'Нет', и калории будут расчитыаны по умолчанию",
        reply_markup=calorie_keyboard)
    return CALORIE_GOAL


def add_city_state(states: Dict[int, Any]):
    states.update({
        CITY: [MessageHandler(filters.Text(), communicate_city)]
    })
