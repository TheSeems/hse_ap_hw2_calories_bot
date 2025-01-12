from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import WEIGHT, HEIGHT
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_weight(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    def update_weight(profile: Profile, weight: int):
        profile.weight = weight

    return await communicate_profile_int(
        update,
        profile_storage,
        update_action=update_weight,
        current_state=WEIGHT,
        next_state=HEIGHT,
        incorrect_input_msg="Пожалуйста, отправьте свой вес в килограммах одним числом",
        next_step_msg="Отлично! Каков ваш рост в сантиметрах?",
    )


def add_weight_state(states: Dict[int, Any]):
    states.update({
        WEIGHT: [MessageHandler(filters.Text(), communicate_weight)]
    })
