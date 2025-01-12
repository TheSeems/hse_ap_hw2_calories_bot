from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, filters, MessageHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import WEIGHT, HEIGHT, AGE, ACTIVITY
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_age(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    def update_age(profile: Profile, age: int):
        profile.age = age

    return await communicate_profile_int(
        update,
        profile_storage,
        update_action=update_age,
        current_state=AGE,
        next_state=ACTIVITY,
        incorrect_input_msg="Пожалуйста, отправьте свой возраст в годах одним числом",
        next_step_msg="Замечательно! Давайте уточним, сколько минут в день вы обычно активны?",
    )


def add_age_state(states: Dict[int, Any]):
    states.update({
        AGE: [MessageHandler(filters.Text(), communicate_age)]
    })
