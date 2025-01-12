import openfoodfacts
from dependency_injector import containers, providers
from pyowm import OWM

from calories_bot.settings import settings
from calories_bot.storage.impl.memory_profile_storage import MemoryProfileStorage
from calories_bot.storage.profile import ProfileStorage


class Dependencies(containers.DeclarativeContainer):
    profile_storage: ProfileStorage = providers.Singleton(MemoryProfileStorage)
    owm: OWM = providers.Singleton(OWM, api_key=settings.openweathermap_token)
    off: openfoodfacts.API = providers.Singleton(
        openfoodfacts.API,
        user_agent="CaloriesBot/1.0",
        country="ru",
        timeout=20,
    )
