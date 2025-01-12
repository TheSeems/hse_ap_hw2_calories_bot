import asyncio

from dependency_injector.wiring import inject, Provide
from pyowm import OWM
from pyowm.weatherapi25.location import Location
from pyowm.weatherapi25.one_call import OneCall

from calories_bot.config.dependencies import Dependencies


@inject
def get_location(
        city: str,
        owm: OWM = Provide[Dependencies.owm],
) -> Location:
    # This cannot be async'ed, because of internal sqlite mess in this library
    return owm.city_id_registry().locations_for(city)[0]


@inject
async def get_weather(
        lat: float,
        lon: float,
        owm: OWM = Provide[Dependencies.owm],
) -> OneCall:
    return await asyncio.to_thread(owm.weather_manager().one_call, lat, lon)


@inject
async def get_temperature(
        lat: float,
        lon: float,
        owm: OWM = Provide[Dependencies.owm],
) -> float:
    return (
        (await asyncio.to_thread(owm.weather_manager().one_call, lat, lon))
        .current.temperature('celsius')["temp"]
    )
