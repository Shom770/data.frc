import asyncio
import itertools
import os
import typing
from types import TracebackType

from dotenv import load_dotenv

from utils import *
from schemas import *


load_dotenv()

__all__ = ["ApiClient"]


class ApiClient:
    """Base class that contains all requests for the TBA API wrapper."""

    def __init__(self, api_key: str = None):
        if api_key is None:
            try:
                api_key = os.environ["TBA_API_KEY"]
            except KeyError:  # In case TBA_API_KEY isn't an environment variable
                api_key = os.environ["API_KEY"]

        self._headers = {"X-TBA-Auth-Key": api_key}

    def __enter__(self) -> "ApiClient":
        BaseSchema._headers = self._headers
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        InternalData.loop.run_until_complete(InternalData.session.close())

    @synchronous
    async def close(self):
        """
        Closes the ongoing session (`aiohttp.ClientSession`).
        Do note that this function should only be used if `persistent_session` was True when initializing this instance.
        """
        await InternalData.session.close()

    async def _get_team_page(
        self,
        page_num: int = None,
        year: typing.Union[range, int] = None,
        simple: bool = False,
        keys: bool = False
    ) -> list[typing.Union[Team, str]]:
        """
        Returns a page of teams (a list of 500 teams or less)

        Parameters:
            page_num:
                An integer that specifies the page number of the list of teams that should be retrieved.
                Teams are paginated by groups of 500, and if page_num is None, every team will be retrieved.
            year:
                An integer that specifies if only the teams that participated during that year should be retrieved.
                If year is a range object, it will return all teams that participated in the years within the range object.
                If year is None, this method will get all teams that have ever participated in the history of FRC.
            simple:
                A boolean that specifies whether the results for each team should be 'shortened' and only contain more relevant information.
            keys:
                A boolean that specifies whether only the names of the FRC teams should be retrieved.

        Returns:
            A list of Team objects for each team in the list.
        """
        async with InternalData.session.get(
                url=construct_url("teams", year=year, page_num=page_num, simple=simple, keys=keys),
                headers=self._headers
        ) as response:
            return [
                Team(**team_data) if not isinstance(team_data, str) else team_data
                for team_data in await response.json()
            ]

    @synchronous
    async def teams(
        self,
        page_num: int = None,
        year: typing.Union[range, int] = None,
        simple: bool = False,
        keys: bool = False
    ) -> list[typing.Union[Team, str]]:
        """
        Retrieves and returns a record of teams based on the parameters given.

        Parameters:
            page_num:
                An integer that specifies the page number of the list of teams that should be retrieved.
                Teams are paginated by groups of 500, and if page_num is None, every team will be retrieved.
            year:
                An integer that specifies if only the teams that participated during that year should be retrieved.
                If year is a range object, it will return all teams that participated in the years within the range object.
                If year is None, this method will get all teams that have ever participated in the history of FRC.
            simple:
                A boolean that specifies whether the results for each team should be 'shortened' and only contain more relevant information.
            keys:
                A boolean that specifies whether only the names of the FRC teams should be retrieved.

        Returns:
            A list of Team objects for each team in the list.
        """
        if simple and keys:
            raise ValueError("simple and keys cannot both be True, you must choose one mode over the other.")

        if isinstance(year, range):
            all_responses = list(
                itertools.chain.from_iterable(
                    await asyncio.gather(
                        *[self.teams.coro(self, page_num, spec_year, simple, keys) for spec_year in year]
                    )
                )
            )

            return sorted(list(set(all_responses)))

        else:
            if page_num:
                return await self._get_team_page(page_num, year, simple, keys)
            else:
                all_teams = itertools.chain.from_iterable(
                    await asyncio.gather(
                        *[self._get_team_page(page_number, year, simple, keys) for page_number in range(0, 20)]
                    )
                )
                return list(all_teams)
