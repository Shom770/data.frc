import asyncio
import itertools
import typing

from .award import Award
from .base_schema import BaseSchema
from .district import District
from .event import Event
from .event_team_status import EventTeamStatus
from .match import Match
from .robot import Robot

try:
    from utils import *
except ImportError:
    from ..utils import *


class Team(BaseSchema):
    """Class representing a team's metadata with methods to get team specific data."""

    def __init__(self, **kwargs):
        self.key: str = kwargs["key"]
        self.team_number: typing.Optional[int] = kwargs.get("team_number")
        self.nickname: typing.Optional[str] = kwargs.get("nickname")
        self.name: typing.Optional[int] = kwargs.get("name")
        self.school_name: typing.Optional[str] = kwargs.get("school_name")
        self.city: typing.Optional[str] = kwargs.get("city")
        self.state_prov: typing.Optional[str] = kwargs.get("state_prov")
        self.country: typing.Optional[str] = kwargs.get("country")
        self.address: typing.Optional[str] = kwargs.get("address")
        self.postal_code: typing.Optional[int] = kwargs.get("postal_code")
        self.gmaps_place_id: typing.Optional[str] = kwargs.get("gmaps_place_id")
        self.gmaps_url: typing.Optional[str] = kwargs.get("gmaps_url")
        self.lat: typing.Optional[float] = kwargs.get("lat")
        self.lng: typing.Optional[float] = kwargs.get("lng")
        self.location_name: typing.Optional[float] = kwargs.get("location_name")
        self.rookie_year: typing.Optional[int] = kwargs.get("rookie_year")
        self.home_championship: typing.Optional[dict] = kwargs.get("home_championship")

        super().__init__()

    async def _get_year_matches(self, year: int, simple: bool, keys: bool) -> list[Match]:
        """
        Retrieves all matches a team played from a certain year.

        Parameters:
            year:
                An integer representing the year to retrieve a team's matches from.
            simple:
                A boolean representing whether each match's information should be stripped to only contain relevant information.
            keys:
                A boolean representing whether only the keys of the matches a team played from said year should be returned:

        Returns:
            A list of Match objects representing each match a team played based on the conditions; might be empty if team didn't play matches that year.
        """
        async with InternalData.session.get(
            url=construct_url("team", key=self.key, endpoint="matches", year=year, simple=simple, keys=keys),
            headers=self._headers
        ) as response:
            if keys:
                return await response.json()
            else:
                return [Match(**match_data) for match_data in await response.json()]

    @synchronous
    async def awards(self, year: typing.Optional[typing.Union[range, int]] = None) -> list[Award]:
        """
        Retrieves all awards a team has gotten either during its career or during certain year(s).

        Parameters:
            year:
                An integer representing a year that the awards should be returned for or a range object representing the years that awards should be returned from. Can be None if no year is passed in as it is an optional parameter.

        Returns:
            A list of Award objects representing each award a team has got based on the parameters; may be empty if the team has gotten no awards.
        """
        async with InternalData.session.get(
            url=construct_url("team", key=self.key, endpoint="awards", year=year if isinstance(year, int) else False),
            headers=self._headers
        ) as response:
            if isinstance(year, range):
                return [Award(**award_data) for award_data in await response.json() if award_data["year"] in year]
            else:
                return [Award(**award_data) for award_data in await response.json()]

    @synchronous
    async def years_participated(self) -> list[int]:
        """
        Returns all the years this team has participated in.

        Returns:
            A list of integers representing every year this team has participated in.
        """
        async with InternalData.session.get(
                url=construct_url("team", key=self.key, endpoint="years_participated"),
                headers=self._headers
        ) as response:
            return await response.json()

    @synchronous
    async def districts(self) -> list[District]:
        """
        Retrieves a list of districts representing each year this team was in said district.

        If a team has never been in a district, the list will be empty.

        Returns:
            A list of districts representing each year this team was in said district if a team has participated in a district, otherwise returns an empty list.
        """
        async with InternalData.session.get(
                url=construct_url("team", key=self.key, endpoint="districts"),
                headers=self._headers
        ) as response:
            return [District(**district_data) for district_data in await response.json()]

    @synchronous
    async def matches(
            self,
            year: typing.Union[range, int],
            simple: typing.Optional[bool] = False,
            keys: typing.Optional[bool] = False
    ) -> list[Match]:
        """
        Retrieves all matches a team played from certain year(s).

        Parameters:
            year:
                An integer representing the year to retrieve a team's matches from or a range object representing all the years matches a team played should be retrieved from.
            simple:
                A boolean representing whether each match's information should be stripped to only contain relevant information. Can be False if `simple` isn't passed in.
            keys:
                A boolean representing whether only the keys of the matches a team played from said year should be returned. Can be False if `keys` isn't passed in.

        Returns:
            A list of Match objects representing each match a team played based on the conditions; might be empty if team didn't play matches in the specified year(s).
        """
        if simple and keys:
            raise ValueError("simple and keys cannot both be True, you must choose one mode over the other.")

        if isinstance(year, range):
            return list(itertools.chain.from_iterable(
                await asyncio.gather(*[self.matches.coro(spec_year, simple, keys) for spec_year in year])
            ))
        else:
            return await self._get_year_matches(year, simple, keys)

    @synchronous
    async def robots(self) -> list[Robot]:
        """
        Retrieves a list of robots representing each robot for every year the team has played if they named the robot.

        If a team has never named a robot, the list will be empty.

        Returns:
            A list of districts representing each year this team was in said district if a team has named a robot, otherwise returns an empty list.
        """
        async with InternalData.session.get(
                url=construct_url("team", key=self.key, endpoint="robots"),
                headers=self._headers
        ) as response:
            return [Robot(**robot_data) for robot_data in await response.json()]

    @synchronous
    async def events(
            self,
            year: typing.Union[range, int] = None,
            simple: bool = False,
            keys: bool = False,
            statuses: bool = False,
    ) -> list[typing.Union[Event, EventTeamStatus, str]]:
        """
        Retrieves and returns a record of teams based on the parameters given.

        Parameters:
            year:
                An integer that specifies if only the events the team participated from that year should be retrieved.
                If year is a range object, it will return all events that the team participated in during that timeframe.
                If year is None, this method will return all events the team has ever participated in.
            simple:
                A boolean that specifies whether the results for each event should be 'shortened' and only contain more relevant information.
            keys:
                A boolean that specifies whether only the names of the events this team has participated in should be returned.
            statuses:
                A boolean that specifies whether a key/value pair of the statuses of events should be returned.

        Returns:
            A list of Event objects for each event that was returned or a list of strings representing the keys of the events or a list of EventTeamStatus objects for each team's status during an event.
        """
        if simple and keys:
            raise ValueError("simple and keys cannot both be True, you must choose one mode over the other.")
        elif statuses and (simple or keys):
            raise ValueError(
                "statuses cannot be True in conjunction with simple or keys, if statuses is True then simple and keys must be False.")
        elif statuses and not year:
            raise ValueError("statuses cannot be True if a year isn't passed into Team.events")

        async with InternalData.session.get(
                url=construct_url(
                    "team", key=self.key, endpoint="events", year=year, simple=simple, keys=keys, statuses=statuses
                ),
                headers=self._headers
        ) as response:
            if keys:
                return await response.json()
            elif not statuses:
                return [Event(**event_data) for event_data in await response.json()]
            else:
                return [
                    EventTeamStatus(event_key, team_status_info)
                    for event_key, team_status_info in (await response.json()).items()
                    if team_status_info
                ]

    @synchronous
    async def event(
            self,
            event_key: str,
            awards: bool = False,
            matches: bool = False,
            simple: bool = False,
            keys: bool = False,
            status: bool = False,
    ) -> typing.Union[list[Award], EventTeamStatus, list[typing.Union[Match, str]]]:
        """
        Retrieves and returns a record of teams based on the parameters given.

        Parameters:
            event_key:
                An event key (a unique key specific to one event) to retrieve data from.
            awards:
                A boolean that specifies whether the awards a team got during a match should be retrieved. Cannot be True in conjunction with `matches`.
            matches:
                A boolean that specifies whether the matches a team played in during an event should be retrieved. Cannot be True in conjunction with `awards`.
            simple:
                A boolean that specifies whether the results for each event's matches should be 'shortened' and only contain more relevant information. Do note that `simple` should only be True in conjunction with `matches`.
            keys:
                A boolean that specifies whether only the keys of the matches the team played should be returned. Do note that `keys` should only be True in conjunction with `matches`
            status:
                A boolean that specifies whether a key/value pair of the status of the team during an event should be returned. `status` should only be the only boolean out of the parameters that is True when using it.

        Returns:
            A list of Match objects representing each match a team played or an EventTeamStatus object to represent the team's status during an event or a list of strings representing the keys of the matches the team played in or a list of Award objects to represent award(s) a team got during an event.
        """
        if not awards and not matches and not status:
            raise ValueError("Either awards, matches or status must be True for this function.")
        elif awards and matches:
            raise ValueError("awards and matches cannot be True, you must choose one endpoint over the other.")
        elif simple and keys:
            raise ValueError("simple and keys cannot both be True, you must choose one mode over the other.")
        elif awards and (simple or keys or matches):
            raise ValueError(
                "awards cannot be True in conjunction with simple, keys or matches, "
                "if awards is True then simple, keys, and matches must be False."
            )
        elif status and (simple or keys or matches):
            raise ValueError(
                "status cannot be True in conjunction with simple, keys or matches "
                "if statuses is True then simple, keys, and matches must be False."
            )

        async with InternalData.session.get(
                url=construct_url(
                    "team",
                    key=self.key,
                    endpoint="event",
                    event_key=event_key,
                    awards=awards,
                    matches=matches,
                    status=status,
                    simple=simple,
                    keys=keys,
                ),
                headers=self._headers
        ) as response:
            if matches and keys:
                return await response.json()
            elif matches:
                return [Match(**match_data) for match_data in await response.json()]
            elif awards:
                return [Award(**award_data) for award_data in await response.json()]
            else:
                return EventTeamStatus(event_key, await response.json())

    def __eq__(self, other) -> bool:
        return self.team_number == other.team_number

    def __hash__(self) -> int:
        return self.team_number

    def __lt__(self, other: "Team") -> bool:
        return self.team_number < other.team_number
