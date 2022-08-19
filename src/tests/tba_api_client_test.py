from hypothesis import given, strategies

from ..api_client import ApiClient


def test_team():
    with ApiClient() as api_client:
        team4099 = api_client.team("frc4099")
        assert team4099.team_number == 4099 and team4099.nickname == "The Falcons"


def test_team_simple():
    with ApiClient() as api_client:
        team4099 = api_client.team("frc4099")
        team4099_simple = api_client.team("frc4099", simple=True)
        assert team4099 != team4099_simple
