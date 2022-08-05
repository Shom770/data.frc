import typing

from .base_schema import BaseSchema
from .district import District
from .event import Event
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
            page_num: int = None,
            year: typing.Union[range, int] = None,
            simple: bool = False,
            keys: bool = False
    ) -> list[typing.Union[Event, str]]:
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

    def __eq__(self, other) -> bool:
        return self.team_number == other.team_number

    def __hash__(self) -> int:
        return self.team_number

    def __lt__(self, other: "Team") -> bool:
        return self.team_number < other.team_number
