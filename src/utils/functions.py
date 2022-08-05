import functools
import typing

from .internal_data import InternalData

__all__ = ["construct_url", "synchronous"]


def construct_url(endpoint, **kwargs) -> str:
    """
    Constructs the URL with the given parameters.

    Parameters:
        endpoint: The base endpoint to add all the different additions to the URL.
        kwargs: Arbritary amount of keyword arguments to construct the URL.

    Returns:
        A string of the constructed URL based on the endpoints.
    """
    return (
            f"https://www.thebluealliance.com/api/v3/{endpoint}/" +
            "/".join(
                map(str, [
                    param_name if isinstance(param_value, bool) else param_value
                    for param_name, param_value in kwargs.items()
                    if param_value is not None and param_value is not False
                ])
            )
    )


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
