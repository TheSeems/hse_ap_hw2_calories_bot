import abc
import contextlib
from typing import Optional, cast, AsyncIterable

from calories_bot.models.profile import Profile, ActiveProfile


class ProfileStorage(abc.ABC):

    @abc.abstractmethod
    async def load_profile(self, user_id: int) -> Profile:
        raise NotImplementedError()

    async def get_active_profile(self, user_id: int) -> Optional[ActiveProfile]:
        profile = await self.load_profile(user_id)
        if not profile.active:
            return None
        return cast(ActiveProfile, profile)

    @contextlib.asynccontextmanager
    async def mutate_profile(self, user_id: int) -> AsyncIterable[Profile]:
        profile = await self.load_profile(user_id)
        yield profile
        await self.save_profile(profile)

    @contextlib.asynccontextmanager
    async def mutate_active_profile(self, user_id: int) -> AsyncIterable[ActiveProfile]:
        profile = await self.get_active_profile(user_id)
        if not profile:
            yield None
            return
        yield profile
        await self.save_profile(profile)

    @abc.abstractmethod
    async def save_profile(self, profile: Profile):
        raise NotImplementedError()
