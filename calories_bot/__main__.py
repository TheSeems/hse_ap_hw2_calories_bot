from telegram import Update
from telegram.ext import Application

from calories_bot.config.dependencies import Dependencies
from calories_bot.settings import configure_logging, settings

from calories_bot.features.start import handler as start_handler
from calories_bot.features.set_profile import handler as set_profile_handler
from calories_bot.features.log_water import handler as log_water_handler
from calories_bot.features.log_food import handler as log_food_handler
from calories_bot.features.log_workout import handler as log_workout_handler
from calories_bot.features.check_progress import handler as check_progress_handler
from calories_bot.features.log_user_messages import handler as log_user_messages_handler

from calories_bot.features.testing.activate_profile import activate_profile_handler


def setup_dependencies():
    container = Dependencies()
    container.wire(packages=["calories_bot.features"])


def add_test_features(application: Application):
    application.add_handler(activate_profile_handler)


def add_features(application: Application):
    application.add_handler(
        log_user_messages_handler,
        # To not hold control flow from other handlers
        group=1,
    )
    application.add_handler(start_handler)
    application.add_handler(set_profile_handler)
    application.add_handler(log_water_handler)
    application.add_handler(log_food_handler)
    application.add_handler(log_workout_handler)
    application.add_handler(check_progress_handler)
    if settings.test_mode:
        add_test_features(application)


def main():
    configure_logging()
    application = Application.builder().token(settings.telegram_token).build()
    setup_dependencies()
    add_features(application)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
