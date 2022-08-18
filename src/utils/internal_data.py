import asyncio

import aiohttp

from .functions import synchronous


class InternalData:
    """Contains internal attributes such as the event loop and the client session."""

    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()

    @synchronous
    async def get(self, *, url: str, headers: dict) -> aiohttp.ClientResponse:
        """
        Sends a GET request to the TBA API.

        Parameters:
            url:
                A string representing which URL to send a GET request to.
            headers:
                A dictionary containing the API key to authorize the request.

        Returns:
            An aiohttp.ClientResponse object representing the response the GET request returned.
        """
        response = self.session.get(url=url, headers=headers)
