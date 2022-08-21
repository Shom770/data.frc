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
        isinstance(chs_comp_alliances, Event.Alliance)
        and all(isinstance(alliance, Event.Alliance) for alliance in chs_comp_alliances)
    )


def test_event_awards():
    """Tests TBA's endpoint that retrieves all awards distributed at an event."""
    chs_comp_awards = Event("2022chcmp").awards()
    assert (
        isinstance(chs_comp_awards, Award)
        and all(isinstance(comp_award, Award) for comp_award in chs_comp_awards)
    )


def test_event_district_points():
    """Tests TBA's endpoint that retrieves the district points distributed to all teams at that event."""
    event_district_points = Event("2022chcmp").district_points()
    assert isinstance(event_district_points, Event.DistrictPoints)


def test_event_district_points_no_return():
    """Tests `Event.DistrictPoints` to ensure that None is returned when there are no district points distributed for an event among teams."""
    comp_district_points = Event("2022cmptx").district_points()
    assert comp_district_points is None
