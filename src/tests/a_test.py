import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_team_frc_number():
    """Tests initializing `Team` via passing in 'frc' then the team number."""
    with ApiClient():
        team4099 = Team("frc", 4099)
        assert team4099.team_number == 4099 and team4099.key == "frc4099"


def test_team_number_frc():
    """Tests initializing `Team` via passing in the team number and then 'frc'."""
    with ApiClient():
        team4099 = Team(4099, "frc")
        assert team4099.team_number == 4099 and team4099.key == "frc4099"


def test_team_number():
    """Tests initializing `Team` via passing in the team number only."""
    with ApiClient():
        team4099 = Team(4099)
        assert team4099.team_number == 4099 and team4099.key == "frc4099"


def test_team_key():
    """Tests initializing `Team` via passing in the team key only."""
    with ApiClient():
        team4099 = Team("frc4099")
        assert team4099.team_number == 4099 and team4099.key == "frc4099"


def test_team_kwarg():
    """Tests initializing `Team` via passing in the team key only as a keyword argument."""
    with ApiClient():
        team4099 = Team(key="frc4099")
        assert team4099.key == "frc4099"
