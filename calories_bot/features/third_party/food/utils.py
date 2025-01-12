import asyncio
from typing import Optional, Tuple

import openfoodfacts
from dependency_injector.wiring import Provide

from calories_bot.config.dependencies import Dependencies


async def find_calories(
        name: str,
        off: openfoodfacts.API = Provide[Dependencies.off],
) -> Optional[Tuple[str, int]]:
    results = await asyncio.to_thread(off.product.text_search, name)
    if results["count"] == 0:
        return None
    product = results["products"][0]
    return product.get('product_name', 'Неизвестно'), product.get('nutriments', {}).get('energy-kcal_100g', 0)
