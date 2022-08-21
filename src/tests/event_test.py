import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_event_one_argument():
    """Tests `Event` with ensuring that an instance is instantiated properly when only the key is passed in as a positional argument."""
    chs_comp = Event("2022chcmp")
    assert chs_comp.key == "2022chcmp"


def test_event_kwarg():
    """Tests `Event` with ensuring that an instance is instantiated properly when the key is passed in as a keyword argument."""
    chs_comp = Event(key="2022chcmp")
    assert chs_comp.key == "2022chcmp"


def test_event_alliances():
    """Tests TBA's endpoint that retrieves all alliances in an event."""
    chs_comp_alliances = Event("2022chcmp").alliances()
    assert (
        isinstance(chs_comp_alliances, list)
        and all(isinstance(alliance, Event.Alliance) for alliance in chs_comp_alliances)
    )


def test_event_awards():
    """Tests TBA's endpoint that retrieves all awards distributed at an event."""
    chs_comp_awards = Event("2022chcmp").awards()
    assert (
        isinstance(chs_comp_awards, list)
        and all(isinstance(comp_award, Award) for comp_award in chs_comp_awards)
    )


def test_event_district_points():
    """Tests TBA's endpoint that retrieves the district points distributed to all teams at that event."""
    event_district_points = Event("2022chcmp").district_points()
    assert isinstance(event_district_points, Event.DistrictPoints)


def test_event_insights():
    """Test TBA's endpoint that retrieves insights about an event."""
    chs_comp_insights = Event("2022chcmp").insights()
    assert isinstance(chs_comp_insights, Event.Insights)


def test_event_matches():
    """Test TBA's endpoint to retrieve all matches that occurred at an event."""
    chs_comp_matches = Event("2022chcmp").matches()
    assert (
        isinstance(chs_comp_matches, list)
        and all(isinstance(comp_match, Match) for comp_match in chs_comp_matches)
    )
