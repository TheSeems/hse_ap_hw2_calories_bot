from telegram.ext import ConversationHandler

from calories_bot.features.log_food.steps.input_gram import add_gram_state
from calories_bot.features.log_food.command import command_handler

states = {}
add_gram_state(states)

handler = ConversationHandler(
    entry_points=[command_handler],
    states=states,
    fallbacks=[],
)
