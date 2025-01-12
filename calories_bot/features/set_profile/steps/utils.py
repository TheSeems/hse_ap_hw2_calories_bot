from asyncio import iscoroutinefunction
from typing import Callable, Optional

from telegram import Update

from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


async def communicate_profile_int(
        update: Update,
        profile_storage: ProfileStorage,
        update_action: Callable[[Profile, int], ...],
        current_state: int,
        next_state: int,
        incorrect_input_msg: str,
        next_step_msg: Optional[str] = None,
) -> int:
    if not update.message:
        return current_state
    value = update.message.text
    if value is None or not value.isnumeric():
        await update.message.reply_text(incorrect_input_msg)
        return current_state
    value = int(value)
    async with profile_storage.mutate_profile(update.message.from_user.id) as profile:
        if iscoroutinefunction(update_action):
            await update_action(profile, value)
        else:
            update_action(profile, value)
    if next_step_msg:
        await update.message.reply_text(next_step_msg)
    return next_state
