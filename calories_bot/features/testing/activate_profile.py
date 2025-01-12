from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.third_party.weather.utils import get_temperature
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def activate_profile(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
):
    current = await profile_storage.load_profile(update.message.from_user.id)
    if current.active:
        return
    profile = Profile(
        user_id=update.message.from_user.id,
        active=True,
        weight=99,
        height=199,
        age=22,
        activity=20,
        city="Moscow",
        lat=55.7522,
        lon=37.6156,
    )
    profile.water_goal = profile.get_default_water_goal(await get_temperature(profile.lat, profile.lon))
    profile.calorie_goal = profile.get_default_calorie_goal()
    await profile_storage.save_profile(profile)


activate_profile_handler = MessageHandler(filters.Text(), activate_profile)
