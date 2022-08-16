import asyncio
import datetime
import itertools
import typing
from dataclasses import dataclass
from statistics import mean

from .award import Award
from .base_schema import BaseSchema
from .event_team_status import EventTeamStatus
from .media import Media
from .robot import Robot

try:
    from utils import *
except ImportError:
    from ..utils import *

__all__ = ["District", "Event", "Match", "Team"]


class District(BaseSchema):
    """Class representing a district containing methods to get specific district information."""

    def __init__(self, **kwargs):
        self.abbreviation: typing.Optional[str] = kwargs.get("abbreviation")
        self.display_name: typing.Optional[str] = kwargs.get("display_name")
        self.key: str = kwargs["key"]
        self.year: typing.Optional[int] = kwargs.get("year")

        super().__init__()


PARSING_FORMAT = "%Y-%m-%d"


class Event(BaseSchema):
    """Class representing an event containing methods to get specific event information."""

    @dataclass()
    class DistrictPoints:
        """Class representing an event's district points given for all teams."""

        points: dict[str, dict[str, int]]
        tiebreakers: dict[str, dict[str, int]]

    @dataclass()
    class Status:
        """Class representing a status of an alliance during an event."""

        playoff_average: float
        level: str
        record: "Event.Record"
        current_level_record: "Event.Record"
        status: str

    @dataclass()
    class Record:
        """Class representing a record of wins, losses and ties for either a certain level or throughout the event."""

        losses: int
        ties: int
        wins: int

    class Alliance(BaseSchema):
        """Class representing an alliance in an event."""

        def __init__(
                self,
                name: str,
                declines: list[str],
                picks: list[str],
                status: dict,
                backup: typing.Optional[dict] = None
        ):
            self.name = name
            self.backup = backup
            self.declines = declines
            self.picks = picks
            self.status: Event.Status = Event.Status(
                playoff_average=status["playoff_average"],
                level=status["level"],
                record=Event.Record(
                    **status["record"]
                ),
                current_level_record=Event.Record(
                    **status["current_level_record"]
                ),
                status=status["status"]
            )

            super().__init__()

    @dataclass()
    class Insights:
        """Class representing the insights of an event (specific by year)"""

        qual: dict
        playoff: dict

    @dataclass()
    class OPRs:
        """Class representing different metrics (OPR/DPR/CCWMs) for teams during an event."""

        oprs: dict
        dprs: dict
        ccwms: dict

        def average(self, metric: typing.Optional[str] = None) -> typing.Union[dict, float]:
            """
            Gets the average of all the metrics for said event; could also only get one average for a specific metric if you aren't interested in all metrics.

            Parameters:
                metric:
                    A string representing which metric to get the average for (opr/dpr/ccwm). `metric` is optional, and if not passed in, the averages for all metrics will be retrieved.

            Returns:
                A dictionary containing the averages for all metrics or a decimal (float object) representing the average of one of the metrics if specified.
            """
            metric_data_mapping = {"opr": self.oprs, "dpr": self.dprs, "ccwm": self.ccwms}

            if metric:
                if metric.lower() not in metric_data_mapping.keys():
                    raise ValueError("metric must be either 'opr', 'dpr', or 'ccwm'")

                metric_data = metric_data_mapping[metric.lower()]

                return mean(metric_data.values())
            else:
                return {
                    "opr": mean(self.oprs.values()),
                    "dpr": mean(self.dprs.values()),
                    "ccwm": mean(self.ccwms.values())
                }

    class ExtraStats:
        """Information about extra statistics regarding the ranking of a team during an event."""

        def __init__(self, extra_stats: list, extra_stats_info: list[dict]):
            self._attributes_formatted = ""

            for data, data_info in zip(extra_stats, extra_stats_info):
                snake_case_name = data_info["name"].lower().replace(" ", "_").replace("+", "plus")

                setattr(self, snake_case_name, data)
                self._attributes_formatted += f"{snake_case_name}={data!r}, "

        def __repr__(self):
            return f"ExtraStats({self._attributes_formatted.rstrip(', ')})"

    class SortOrders:
        """Information about the team used to determine ranking for an event."""

        def __init__(self, sort_orders: list, sort_order_info: list[dict]):
            self._attributes_formatted = ""

            for data, data_info in zip(sort_orders, sort_order_info):
                snake_case_name = data_info["name"].lower().replace(" ", "_").replace("+", "plus")

                setattr(self, snake_case_name, data)
                self._attributes_formatted += f"{snake_case_name}={data!r}, "

        def __repr__(self):
            return f"SortOrders({self._attributes_formatted.rstrip(', ')})"

    @dataclass()
    class Ranking:
        """Class representing a team's ranking during an event."""

        dq: int
        extra_stats: "Event.ExtraStats"
        matches_played: int
        qual_average: int
        rank: int
        record: "Event.Record"
        sort_orders: "Event.SortOrders"
        team_key: str

    @dataclass()
    class Webcast:
        """Class representing metadata and information about a webcast for an event."""

        type: str
        channel: str
        date: typing.Optional[datetime.datetime] = None
        file: typing.Optional[str] = None

        def __post_init__(self):
            if self.date:
                self.date = datetime.datetime.strptime(self.date, PARSING_FORMAT)

    def __init__(self, **kwargs):
        self.key: str = kwargs["key"]
        self.name: typing.Optional[str] = kwargs.get("name")
        self.event_code: typing.Optional[str] = kwargs.get("event_code")
        self.event_type: typing.Optional[int] = kwargs.get("event_type")

        district_data = kwargs.get("district")
        self.district: typing.Optional[dict] = District(**district_data) if district_data else None

        self.city: typing.Optional[str] = kwargs.get("city")
        self.state_prov: typing.Optional[str] = kwargs.get("state_prov")
        self.country: typing.Optional[str] = kwargs.get("country")

        try:
            self.start_date: typing.Optional[datetime.datetime] = datetime.datetime.strptime(
                kwargs["start_date"], PARSING_FORMAT
            )
            self.end_date: typing.Optional[datetime.datetime] = datetime.datetime.strptime(
                kwargs["end_date"], PARSING_FORMAT
            )
        except KeyError:
            self.start_date = None
            self.end_date = None

        self.year: typing.Optional[int] = kwargs.get("year")

        self.short_name: typing.Optional[str] = kwargs.get("short_name")
        self.event_type_string: typing.Optional[str] = kwargs.get("event_type_string")
        self.week: typing.Optional[int] = kwargs.get("week")

        self.address: typing.Optional[str] = kwargs.get("address")
        self.postal_code: typing.Optional[str] = kwargs.get("postal_code")
        self.gmaps_place_id: typing.Optional[str] = kwargs.get("gmaps_place_id")
        self.gmaps_url: typing.Optional[str] = kwargs.get("gmaps_url")
        self.lat: typing.Optional[float] = kwargs.get("lat")
        self.lng: typing.Optional[float] = kwargs.get("lng")
        self.location_name: typing.Optional[str] = kwargs.get("location_name")
        self.timezone: typing.Optional[str] = kwargs.get("timezone")

        self.website: typing.Optional[str] = kwargs.get("website")

        self.first_event_id: typing.Optional[str] = kwargs.get("first_event_id")
        self.first_event_code: typing.Optional[str] = kwargs.get("first_event_code")

        self.webcasts: typing.Optional[list] = [
            self.Webcast(**webcast_data) for webcast_data in kwargs.get("webcasts", []) if webcast_data
        ]

        self.division_keys: typing.Optional[list] = kwargs.get("division_keys")
        self.parent_event_key: typing.Optional[str] = kwargs.get("parent_event_key")

        self.playoff_type: typing.Optional[int] = kwargs.get("playoff_type")
        self.playoff_type_string: typing.Optional[str] = kwargs.get("playoff_type_string")

        super().__init__()

    @synchronous
    async def alliances(self) -> list[Alliance]:
        """
        Retrieves all alliances of an event.

        Returns:
            A list of Alliance objects representing each alliance in the event.
        """
        async with InternalData.session.get(
                url=construct_url("event", key=self.key, endpoint="alliances"),
                headers=self._headers
        ) as response:
            return [self.Alliance(**alliance_info) for alliance_info in await response.json()]

    @synchronous
    async def awards(self) -> list[Award]:
        """
        Retrieves all awards distributed in an event.

        Returns:
            A list of Award objects representing each award distributed in an event.
        """
        async with InternalData.session.get(
            url=construct_url("event", key=self.key, endpoint="awards"),
            headers=self._headers
        ) as response:
            return [Award(**award_info) for award_info in await response.json()]

    @synchronous
    async def district_points(self) -> typing.Optional[DistrictPoints]:
        """
        Retrieves district points for teams during an event for both qualification and tiebreaker matches.

        Returns:
            A DistrictPoints object containing "points" and "tiebreakers" fields, with each field possessing a dictionary mapping team keys to their points or None if the event doesn't take place in a district or district points are not applicable to the event.
        """
        async with InternalData.session.get(
                url=construct_url("event", key=self.key, endpoint="district_points"),
                headers=self._headers
        ) as response:
            event_district_points = await response.json()

            if event_district_points:
                return self.DistrictPoints(**event_district_points)

    @synchronous
    async def insights(self) -> typing.Optional[Insights]:
        """
        Retrieves insights of an event (specific data about performance and the like at the event; specific by game).
        Insights can only be retrieved for any events from 2016 and onwards.

        Returns:
            An Insight object containing qualification and playoff insights from the event. Can be None if the event hasn't occurred yet, and the fields of Insight may be None depending on how far the event has advanced.
        """
        async with InternalData.session.get(
                url=construct_url("event", key=self.key, endpoint="insights"),
                headers=self._headers
        ) as response:
            insights = await response.json()

            if insights:
                return self.Insights(**insights)

    @synchronous
    async def oprs(self) -> OPRs:
        """
        Retrieves different metrics for all teams during an event.
        To see an explanation on OPR and other metrics retrieved from an event, see https://www.thebluealliance.com/opr.

        Returns:
            An OPRs object containing a key/value pair for the OPRs, DPRs, and CCWMs of all teams at an event. The fields of `OPRs` may be empty if OPRs, DPRs, and CCWMs weren't calculated.
        """
        async with InternalData.session.get(
            url=construct_url("event", key=self.key, endpoint="oprs"),
            headers=self._headers
        ) as response:
            metric_data = await response.json()

            if metric_data:
                return self.OPRs(**await response.json())
            else:
                return self.OPRs(oprs={}, dprs={}, ccwms={})

    @synchronous
    async def predictions(self) -> dict:
        """
        Retrieves predictions for matches of an event. May not work for all events since this endpoint is in beta per TBA.

        Returns:
            A dictionary containing the predictions of an event from TBA (contains year-specific information). May be an empty dictionary if there are no predictions available for that event.
        """
        async with InternalData.session.get(
            url=construct_url("event", key=self.key, endpoint="predictions"),
            headers=self._headers
        ) as response:
            return await response.json()

    @synchronous
    async def rankings(self) -> dict[str, Ranking]:
        """
        Retrieves a list of team rankings for an event.

        Returns:
            A dictionary with team keys as the keys of the dictionary and Ranking objects for that team's information about their ranking at an event as values of the dictionary.
        """
        async with InternalData.session.get(
                url=construct_url("event", key=self.key, endpoint="rankings"),
                headers=self._headers
        ) as response:
            rankings_info = await response.json()
            rankings_dict = {}

            for rank_info in rankings_info["rankings"]:
                rank_info["extra_stats"] = self.ExtraStats(
                    rank_info["extra_stats"],
                    rankings_info["extra_stats_info"]
                )
                rank_info["sort_orders"] = self.SortOrders(
                    rank_info["sort_orders"],
                    rankings_info["sort_order_info"]
                )

                rankings_dict[rank_info["team_key"]] = self.Ranking(**rank_info)

            return rankings_dict


class Match(BaseSchema):
    """Class representing a match's metadata with methods to get match specific data."""

    @dataclass()
    class Alliance:
        """Class representing an alliance's performance/metadata during a match."""

        score: typing.Optional[int]
        team_keys: list[str]
        surrogate_team_keys: list[str]
        dq_team_keys: list[str]

    def __init__(self, **kwargs):
        self.key: str = kwargs["key"]

        self.comp_level: typing.Optional[str] = kwargs.get("comp_level")
        self.set_number: typing.Optional[int] = kwargs.get("set_number")

        self.match_number: typing.Optional[int] = kwargs.get("match_number")

        alliances = kwargs.get("alliances")
        self.alliances: typing.Optional[dict] = {
            "red": self.Alliance(**alliances["red"]),
            "blue": self.Alliance(**alliances["blue"])
        }
        self.winning_alliance: typing.Optional[str] = kwargs.get("winning_alliance")

        self.event_key: typing.Optional[str] = kwargs.get("event_key")

        time = kwargs.get("time")
        actual_time = kwargs.get("actual_time")
        predicted_time = kwargs.get("predicted_time")
        post_result_time = kwargs.get("post_result_time")

        self.time: typing.Optional[datetime.datetime] = (
            datetime.datetime.fromtimestamp(time) if time else None
        )
        self.actual_time: typing.Optional[int] = (
            datetime.datetime.fromtimestamp(actual_time) if actual_time else None
        )
        self.predicted_time: typing.Optional[int] = (
            datetime.datetime.fromtimestamp(predicted_time) if predicted_time else None
        )
        self.post_result_time: typing.Optional[int] = (
            datetime.datetime.fromtimestamp(post_result_time) if post_result_time else None
        )

        self.score_breakdown: typing.Optional[dict] = kwargs.get("score_breakdown")
        self.videos: typing.Optional[list] = kwargs.get("videos")

        super().__init__()


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

    async def _get_year_media(self, year: int, media_tag: typing.Optional[str] = None) -> list[Media]:
        """
        Retrieves all the media of a certain team from a certain year and based off the media_tag if passed in.

        Parameters:
            year:
                An integer representing a year to retrieve a team's media from.
            media_tag:
                A string representing the type of media to be returned. Can be None if media_tag is not passed in.

        Returns:
            A list of Media objects representing individual media from a team during a year.
        """
        if media_tag:
            url = construct_url(
                "team", key=self.key,
                endpoint="media", second_endpoint="tag",
                media_tag=media_tag, year=year
            )
        else:
            url = construct_url("team", key=self.key, endpoint="media", year=year)

        async with InternalData.session.get(url=url, headers=self._headers) as response:
            return [Media(**media_data) for media_data in await response.json()]

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
                url=construct_url("team", key=self.key, endpoint="awards",
                                  year=year if isinstance(year, int) else False),
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
                await asyncio.gather(*[self.matches.coro(self, spec_year, simple, keys) for spec_year in year])
            ))
        else:
            return await self._get_year_matches(year, simple, keys)

    @synchronous
    async def media(self, year: typing.Union[range, int], media_tag: typing.Optional[str] = None) -> list[Media]:
        """
        Retrieves all the media of a certain team based off the parameters.

        Parameters:
            year:
                An integer representing a year to retrieve a team's media from or a range object representing all the years media from a team should be retrieved from.
            media_tag:
                A string representing the type of media to be returned. Can be None if media_tag is not passed in.

        Returns:
            A list of Media objects representing individual media from a team.
        """
        if isinstance(year, range):
            return list(itertools.chain.from_iterable(
                await asyncio.gather(*[self.media.coro(self, spec_year, media_tag) for spec_year in year])
            ))
        else:
            return await self._get_year_media(year, media_tag)

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

    @synchronous
    async def social_media(self) -> list[Media]:
        """
        Retrieves all social media accounts of a team registered on TBA.

        Returns:
            A list of Media objects representing each social media account of a team. May be empty if a team has no social media accounts.
        """
        async with InternalData.session.get(
                url=construct_url("team", key=self.key, endpoint="social_media"),
                headers=self._headers
        ) as response:
            return [Media(**social_media_info) for social_media_info in await response.json()]

    def __eq__(self, other) -> bool:
        return self.team_number == other.team_number

    def __hash__(self) -> int:
        return self.team_number

    def __lt__(self, other: "Team") -> bool:
        return self.team_number < other.team_number