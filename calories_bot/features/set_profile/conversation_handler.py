from telegram.ext import ConversationHandler
from calories_bot.features.set_profile.command import command_handler
from calories_bot.features.set_profile.steps.activity import add_activity_state
from calories_bot.features.set_profile.steps.age import add_age_state
from calories_bot.features.set_profile.steps.calorie_goal import add_calorie_goal
from calories_bot.features.set_profile.steps.cancel import cancel_handler
from calories_bot.features.set_profile.steps.city import add_city_state
from calories_bot.features.set_profile.steps.height import add_height_state
from calories_bot.features.set_profile.steps.weight import add_weight_state

states = {}
add_weight_state(states)
add_height_state(states)
add_age_state(states)
add_activity_state(states)
add_city_state(states)
add_calorie_goal(states)

handler = ConversationHandler(
    entry_points=[command_handler],
    states=states,
    fallbacks=[cancel_handler],
)
