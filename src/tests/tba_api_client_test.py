import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_api_status():
    with ApiClient() as api_client:
        tba_api_status = api_client.status()
        assert isinstance(tba_api_status, APIStatus)


def test_districts():
    with ApiClient() as api_client:
        all_districts = api_client.districts(year=2022)
        assert isinstance(all_districts, list) and all(isinstance(district, District) for district in all_districts)


def test_team():
    with ApiClient() as api_client:
        team4099 = api_client.team("frc4099")
        assert team4099.team_number == 4099 and team4099.nickname == "The Falcons"


def test_team_simple():
    with ApiClient() as api_client:
        team4099 = api_client.team("frc4099")
        team4099_simple = api_client.team("frc4099", simple=True)
        assert team4099 != team4099_simple


def test_team_not_existing():
    with pytest.raises(TBAError, match="is not a valid team key"):
        with ApiClient() as api_client:
            api_client.team("frc0")


def test_event():
    with ApiClient() as api_client:
        cmp2022 = api_client.event("2022cmptx")
        assert cmp2022.name == "Einstein Field"


def test_event_simple():
    with ApiClient() as api_client:
        cmp2022 = api_client.event("2022cmptx")
        cmp2022_simple = api_client.event("2022cmptx", simple=True)
        assert cmp2022 != cmp2022_simple


def test_event_not_existing():
    with pytest.raises(TBAError, match="is not a valid event key"):
        with ApiClient() as api_client:
            api_client.event(event_key="Event Doesn't Exist")


def test_events():
    with ApiClient() as api_client:
        chs_cmp = api_client.events(year=2022)
        assert isinstance(chs_cmp, list) and all(isinstance(event, Event) for event in chs_cmp)


def test_events_range():
    with ApiClient() as api_client:
        all_events = api_client.events(year=range(2020, 2023))
        assert isinstance(all_events, list) and all(isinstance(event, Event) for event in all_events)


def test_events_simple():
    with ApiClient() as api_client:
        all_events = api_client.events(year=2022)
        all_events_simple = api_client.events(year=2022, simple=True)
        assert all_events != all_events_simple


def test_events_keys():
    with ApiClient() as api_client:
        all_event_keys = api_client.events(year=2022, keys=True)
        assert isinstance(all_event_keys, list) and all(isinstance(event_key, str) for event_key in all_event_keys)
