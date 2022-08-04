import functools
import typing

import aiohttp

from ..api_client import ApiClient

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
        if not self.session:
            self.session = aiohttp.ClientSession()

        result = self._loop.run_until_complete(coro(self, *args, **kwargs))

        if not self._persistent_session:
            self._loop.run_until_complete(self.session.close())
            self.session = None

        return result

    return wrapper
