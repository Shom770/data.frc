import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_district_year_abbreviation():
    """Tests initializing `District` via passing in the year and then the abbreviation (eg District(2022, 'chs'))."""
    with ApiClient():
        chs_district = District(2022, "chs")
        assert chs_district.year == 2022 and chs_district.abbreviation == "chs" and chs_district.key == "2022chs"


def test_district_key():
    """Tests initializing `District` via passing in the district key (eg '2022chs')."""
    with ApiClient():
        chs_district = District("2022chs")
        assert chs_district.year == 2022 and chs_district.abbreviation == "chs" and chs_district.key == "2022chs"


def test_district_kwargs():
    """Tests initializing `District` via passing in keyword arguments."""
    with ApiClient():
        chs_district = District(key="2022chs")
        assert chs_district.year == 2022 and chs_district.abbreviation == "chs" and chs_district.key == "2022chs"


def test_district_events():
    """Tests TBA's endpoint to retrieve all events that occurred in a district."""
    with ApiClient():
        chs_events = District(2022, "chs").events()
        assert isinstance(chs_events, list) and all(isinstance(event, Event) for event in chs_events)


def test_district_events_simple():
    """Tests TBA's endpoint to retrieve shortened information about the events that occurred in a district."""
    with ApiClient():
        chs_district = District(2022, "chs")
        assert chs_district.events() != chs_district.events(simple=True)
