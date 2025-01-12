from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, filters, MessageHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.set_profile.states import WEIGHT, HEIGHT, AGE
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_height(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    def update_height(profile: Profile, height: int):
        profile.height = height

    return await communicate_profile_int(
        update,
        profile_storage,
        update_action=update_height,
        current_state=HEIGHT,
        next_state=AGE,
        incorrect_input_msg="Пожалуйста, отправьте свой рост одним числом",
        next_step_msg="Отлично! Сколько Вам полных лет?",
    )


def add_height_state(states: Dict[int, Any]):
    states.update({
        HEIGHT: [MessageHandler(filters.Text(), communicate_height)]
    })
