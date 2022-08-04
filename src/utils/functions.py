import functools
import typing

import aiohttp

__all__ = ["synchronous"]


def synchronous(coro: typing.Callable) -> typing.Callable:
    """
    Decorator that wraps an asynchronous function around a synchronous function.
    Users can call the function synchronously although its internal behavior is asynchronous for efficiency.

    Parameters:
        coro: A coroutine that is passed into the decorator.

    Returns:
        A synchronous function with its internal behavior being asynchronous.
    """

    @functools.wraps(coro)
    def wrapper(self, *args, **kwargs) -> typing.Any:
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            result = self._loop.run_until_complete(coro(self, *args, **kwargs))
        except AttributeError:
            if not self.parent_api_client.session:
                self.parent_api_client.session = aiohttp.ClientSession()
            result = self.parent_api_client._loop.run_until_complete(coro(self, *args, **kwargs))

        try:
            if not self._persistent_session:
                self._loop.run_until_complete(self.session.close())
                self.session = None
        except AttributeError:
            if not self.parent_api_client._persistent_session:
                self.parent_api_client._loop.run_until_complete(self.session.close())
                self.parent_api_client.session = None

        return result

    return wrapper
