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
        BaseSchema.add_headers(self._headers)

    def __enter__(self) -> "ApiClient":
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

    async def _get_year_events(
            self,
            year: int,
            simple: typing.Optional[bool] = False,
            keys: typing.Optional[bool] = False
    ) -> list[typing.Union[Event, str]]:
        """
        Retrieves all the events from a year.

        Parameters:
            year:
                An integer representing which year to return its events for.
            simple:
                A boolean representing whether some of the information regarding an event should be stripped to only contain relevant information about the event.
            keys:
                A boolean representing whether only the keys of the events should be returned.

        Returns:
            A list of Event objects representing each event in a year or a list of strings representing all the keys of the events retrieved.
        """
        async with InternalData.session.get(
                url=construct_url("events", year=year, simple=simple, keys=keys),
                headers=self._headers
        ) as response:
            if keys:
                return await response.json()
            else:
                return [Event(**event_data) for event_data in await response.json()]

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
    async def events(
            self,
            year: typing.Union[range, int],
            simple: typing.Optional[bool] = False,
            keys: typing.Optional[bool] = False
    ) -> list[typing.Union[Event, str]]:
        """
        Retrieves all the events from certain year(s).

        Parameters:
            year:
                An integer representing which year to return its events for o range object representing all the years events should be returned from.
            simple:
                A boolean representing whether some of the information regarding an event should be stripped to only contain relevant information about the event.
            keys:
                A boolean representing whether only the keys of the events should be returned.

        Returns:
            A list of Event objects representing each event in certain year(s) or a list of strings representing all the keys of the events retrieved.
        """
        if isinstance(year, range):
            return list(
                itertools.chain.from_iterable(
                    await asyncio.gather(
                        *[self.events.coro(self, spec_year, simple, keys) for spec_year in year]
                    )
                )
            )
        else:
            return await self._get_year_events(year, simple, keys)

    @synchronous
    async def team(
            self,
            team_key: str,
            simple: bool = False
    ) -> Team:
        """
        Retrieves and returns a record of teams based on the parameters given.

        Parameters:
            team_key:
                A string representing a unique key assigned to a team to set it apart from others (in the form of frcXXXX) where XXXX is the team number.
            simple:
                A boolean that specifies whether the results for the team should be 'shortened' and only contain more relevant information.

        Returns:
            A Team object representing the data given.
        """
        async with InternalData.session.get(
            url=construct_url("team", key=team_key, simple=simple),
            headers=self._headers
        ) as response:
            return Team(**await response.json())

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
