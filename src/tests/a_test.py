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
        assert team4099.key == "frc4099" and team4099.team_number == 4099


def test_team_awards():
    """Tests TBA's endpoint to retrieve all awards a team has gotten over its career."""
    with ApiClient():
        team4099_awards = Team(4099).awards()
        assert (
            isinstance(team4099_awards, list)
            and all(isinstance(team_award, Award) for team_award in team4099_awards)
        )


def test_team_awards_year():
    """Tests TBA's endpoint to retrieve all awards a team has gotten in a certain year."""
    with ApiClient():
        team4099_awards = Team(4099).awards(2022)
        assert (
            isinstance(team4099_awards, list)
            and all(isinstance(team_award, Award) for team_award in team4099_awards)
        )


def test_team_awards_range():
    """Tests `Team.awards` with passing in a range object into the `year` parameter to retrieve awards a team recieved across multiple years."""
    with ApiClient():
        team4099_awards = Team(4099).awards(range(2020, 2023))
        assert (
            isinstance(team4099_awards, list)
            and all(isinstance(team_award, Award) for team_award in team4099_awards)
        )


def test_team_years_participated():
    """Tests TBA's endpoint to retrieve all the years a team played in."""
    with ApiClient():
        team4099_years_participated = Team(4099).years_participated()
        assert isinstance(team4099_years_participated, list) and min(team4099_years_participated) == 2012


def test_team_districts():
    """Tests TBA's endpoint to retrieve all the districts the team has ever played in (eg 2020chs, 2021chs, ...)"""
    with ApiClient():
        team4099_districts = Team(4099).districts()
        assert (
            isinstance(team4099_districts, list)
            and all(isinstance(team_district, District) for team_district in team4099_districts)
        )


def test_team_matches():
    """Tests TBA's endpoint to retrieve all the matches a team played in a certain year."""
    with ApiClient():
        rapid_react_matches = Team(4099).matches(2022)
        assert (
            isinstance(rapid_react_matches, list)
            and all(isinstance(game_match, Match) for game_match in rapid_react_matches)
        )


def test_team_matches_range():
    """Tests `Team.matches` to pass in a range object for the `year` parameter to retrieve matches a team played over multiple years."""
    team4099_matches = Team(4099).matches(range(2020, 2023))
    assert (
            isinstance(team4099_matches, list)
            and all(isinstance(game_match, Match) for game_match in team4099_matches)
    )


def test_team_matches_event_code():
    """Tests `Team.matches` to retrieve all the matches a team played in a certain event."""
    with ApiClient():
        team4099_iri_matches = Team(4099).matches(2022, "iri")
        assert (
            isinstance(team4099_iri_matches, list)
            and all(isinstance(game_match, Match) for game_match in team4099_iri_matches)
        )


def test_team_matches_simple():
    """Tests TBA's endpoint to retrieve shortened information about all the matches a team played in a certain year."""
    with ApiClient():
        rapid_react_matches = Team(4099).matches(2022, simple=True)
        assert (
            isinstance(rapid_react_matches, list)
            and all(isinstance(game_match, Match) for game_match in rapid_react_matches)
        )


def test_team_matches_keys():
    """Tests TBA's endpoint to retrieve the keys of all the matches a team played in a certain year."""
    with ApiClient():
        rapid_react_matches = Team(4099).matches(2022, keys=True)
        assert (
            isinstance(rapid_react_matches, list)
            and all(isinstance(match_key, str) for match_key in rapid_react_matches)
        )


def test_team_matches_extra_parameters():
    """Tests `Team.matches` to ensure that an error is raised when simple and keys are both True.."""
    with pytest.raises(ValueError):
        with ApiClient():
            Team(4099).matches(2022, simple=True, keys=True)
