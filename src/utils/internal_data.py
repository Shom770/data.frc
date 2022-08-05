import asyncio

import aiohttp


class InternalData:
    """Contains internal attributes such as the event loop and the client session."""

    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
