import typing

from .base_schema import BaseSchema
from .district import District
from .event import Event
from .event_team_status import EventTeamStatus
from .robot import Robot

try:
    from utils import *
except ImportError:
    from ..utils import *


class Team(BaseSchema):
    """Class representing a team's metadata with methods to get team specific data."""

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
            A list of Event objects for each event that was returned, a list of strings representing the keys of the events, or a list of EventTeamStatus objects for each team's status during an event.
        """
        if simple and keys:
            raise ValueError("simple and keys cannot both be True, you must choose one mode over the other.")
        elif statuses and (simple or keys):
            raise ValueError("statuses cannot be True in conjunction with simple or keys, if statuses is True then simple and keys must be False.")
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

    def __eq__(self, other) -> bool:
        return self.team_number == other.team_number

    def __hash__(self) -> int:
        return self.team_number

    def __lt__(self, other: "Team") -> bool:
        return self.team_number < other.team_number
