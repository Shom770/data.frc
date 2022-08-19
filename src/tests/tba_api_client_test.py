from hypothesis import given, settings, strategies

from ..api_client import ApiClient
from ..schemas import *


@given(strategies.integers(min_value=1990, max_value=2022))
@settings(deadline=None)
def test_districts(year: int):
    with ApiClient() as api_client:
        all_districts = api_client.districts(year)
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
