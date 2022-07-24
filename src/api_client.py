import asyncio
import itertools
import os
import typing

import aiohttp
from dotenv import load_dotenv


load_dotenv()


class ApiClient:
    """Base class that contains all synchronous requests for the TBA API wrapper."""

    _loop = asyncio.get_event_loop()

    def __init__(self, api_key: str = None):
        if api_key is None:
            try:
                api_key = os.environ["TBA_API_KEY"]
            except KeyError:  # In case TBA_API_KEY isn't an environment variable
                api_key = os.environ["API_KEY"]

        self._headers = {"X-TBA-Auth-Key": api_key}
        self._base_url = "https://www.thebluealliance.com/api/v3/"

    def _construct_url(self, endpoint, **kwargs) -> str:
        """
        Constructs the URL with the given parameters.

        Parameters:
            endpoint: The base endpoint to add all the different additions to the URL.
            kwargs: Arbritary amount of keyword arguments to construct the URL.

        Returns:
            A string of the constructed URL based on the endpoints.
        """
        return (
            f"{self._base_url}{endpoint}/" +
            "/".join(
                map(str, [
                    param_name if isinstance(param_value, bool) else param_value
                    for param_name, param_value in kwargs.items()
                    if param_value is not None and param_value is not False
                ])
            )
         )

    async def _get_team(
        self,
        page_num: int = None,
        year: typing.Union[range, int] = None,
        simple: bool = False,
        keys: bool = False
    ) -> list:
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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self._construct_url("teams", year=year, page_num=page_num, simple=simple, keys=keys),
                headers=self._headers
            ) as response:
                return await response.json()

    async def _async_teams(
        self,
        page_num: int = None,
        year: typing.Union[range, int] = None,
        simple: bool = False,
        keys: bool = False
    ) -> list:
        """
        Asynchronous implementation of the .teams method for efficiency.

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
                        *[self.teams(page_num, spec_year, simple, keys) for spec_year in year]
                    )
                )
            )

            try:
                return sorted(list(set(all_responses)))
            except TypeError:
                return [dict(team) for team in {tuple(team.items()) for team in all_responses}]

        else:
            if page_num:
                return await self._get_team(page_num, year, simple, keys)
            else:
                all_teams = itertools.chain.from_iterable(
                    await asyncio.gather(
                        *[self._get_team(page_number, year, simple, keys) for page_number in range(0, 20)]
                    )
                )
                return list(all_teams)

    def teams(
        self,
        page_num: int = None,
        year: typing.Union[range, int] = None,
        simple: bool = False,
        keys: bool = False
    ) -> list:
        """
        Gets a record of all FRC teams and filters them based on certain parameters.

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
        return self._loop.run_until_complete(
            self._async_teams(page_num, year, simple, keys)
        )
