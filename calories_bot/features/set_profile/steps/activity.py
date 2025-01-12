from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import WEIGHT, HEIGHT, AGE, ACTIVITY, CITY
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_activity(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    def update_activity(profile: Profile, activity: int):
        profile.activity = activity

    return await communicate_profile_int(
        update,
        profile_storage,
        update_action=update_activity,
        current_state=ACTIVITY,
        next_state=CITY,
        incorrect_input_msg="Пожалуйста, отправьте количество минут в день когда вы активны одним числом",
        next_step_msg="Отлично! В каком городе Вы находитесь?",
    )


def add_activity_state(states: Dict[int, Any]):
    states.update({
        ACTIVITY: [MessageHandler(filters.Text(), communicate_activity)]
    })
