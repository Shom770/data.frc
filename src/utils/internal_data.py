import asyncio
import typing

import aiohttp


class InternalData:
    """Contains internal attributes such as the event loop and the client session."""

    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()

    @classmethod
    async def get(cls, *, url: str, headers: dict) -> typing.Union[list, dict]:
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
        async with cls.session.get(url=url, headers=headers) as response:
            response_json = await response.json()

            if isinstance(response_json, dict) and response_json.get("Error"):
                raise Exception(response_json["Error"])
            else:
                return response_json
