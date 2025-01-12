from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.log_food.states import INPUT_GRAM
from calories_bot.features.set_profile.steps.utils import communicate_profile_int
from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


@inject
async def communicate_gram(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
) -> int:
    async def update_gram(profile: Profile, weight: int):
        addend = (1. * weight / 100) * context.user_data["selected_product"]["calories"]
        profile.logged_calories += addend
        await update.message.reply_text(f"Записано {round(addend, 2)} ккал.")
        del context.user_data['selected_product']

    return await communicate_profile_int(
        update,
        profile_storage,
        update_action=update_gram,
        current_state=INPUT_GRAM,
        next_state=ConversationHandler.END,
        incorrect_input_msg="Пожалуйста, отправьте сколько грамм продукта было съедено",
    )


def add_gram_state(states: Dict[int, Any]):
    states.update({
        INPUT_GRAM: [MessageHandler(filters.Text(), communicate_gram)]
    })
