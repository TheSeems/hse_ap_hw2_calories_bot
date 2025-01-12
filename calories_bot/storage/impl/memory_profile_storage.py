from typing import Optional, Dict

from calories_bot.models.profile import Profile
from calories_bot.storage.profile import ProfileStorage


class MemoryProfileStorage(ProfileStorage):
    def __init__(self):
        self._map: Dict[int, Profile] = {}

    async def load_profile(self, user_id: int) -> Optional[Profile]:
        if user_id not in self._map:
            profile = Profile(user_id=user_id)
            self._map[user_id] = profile
            return profile
        return self._map[user_id]

    async def save_profile(self, profile: Profile):
        self._map[profile.user_id] = profile
