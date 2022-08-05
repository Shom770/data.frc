import functools
import typing

from .internal_data import InternalData

__all__ = ["synchronous"]


def synchronous(coro: typing.Coroutine) -> typing.Callable:
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
        return InternalData.loop.run_until_complete(coro(self, *args, **kwargs))

    wrapper.coro = coro

    return wrapper
