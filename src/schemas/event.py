import datetime
import typing
from dataclasses import dataclass

from .base_schema import BaseSchema
from .district import District

try:
    from utils import *
except ImportError:
    from ..utils import *

PARSING_FORMAT = "%Y-%m-%d"


class Event(BaseSchema):
    """Class representing an event containing methods to get specific event information."""

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
