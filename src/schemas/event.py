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

    @dataclass
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

        self.start_date: typing.Optional[datetime.datetime] = datetime.datetime.strptime(
            kwargs.get("start_date"), PARSING_FORMAT
        )
        self.end_date: typing.Optional[datetime.datetime] = datetime.datetime.strptime(
            kwargs.get("end_date"), PARSING_FORMAT
        )
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
