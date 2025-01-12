from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from calories_bot.config.dependencies import Dependencies
from calories_bot.features.log_food.states import INPUT_GRAM
from calories_bot.features.third_party.food.utils import find_calories
from calories_bot.storage.profile import ProfileStorage


@inject
async def log_food(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        profile_storage: ProfileStorage = Provide[Dependencies.profile_storage],
):
    if not update.message:
        return
    if (await profile_storage.get_active_profile(update.message.from_user.id)) is None:
        await update.message.reply_text("Сначала заполните профиль: /set_profile")
        return
    if len(context.args) == 0:
        await update.message.reply_text("Введите название продукта")
        return
    product_name = context.args[0]
    await update.message.reply_text(f"Ищем '{product_name}'...")
    try:
        product = await find_calories(product_name)
    except Exception as e:
        await update.message.reply_text(f"К сожалению, при поиске что-то пошло не так: {str(e)}. "
                                        f"Попробуйте подождать или ввести другой запрос")
        return
    if product is None:
        await update.message.reply_text(f"Продукт не найден: '{product_name}'")
        return
    (name, calories) = product
    context.user_data["selected_product"] = {"name": name, "calories": calories}
    await update.message.reply_text(f"{name} - {calories}ккал. на 100г. Введите количество грамм одним числом")
    return INPUT_GRAM


command_handler = CommandHandler("log_food", log_food)
