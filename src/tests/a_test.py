import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_team_frc_number():
    """Tests initializing `Team` via passing in 'frc' then the team number."""
    with ApiClient():
        team4099 = Team("frc", 4099)
        assert team4099.team_number == 4099 and team4099.key == "frc4099"


def test_district_year_abbreviation_reversed():
    """Tests initializing `District` via passing in the abbreviation and then the year (eg District('chs', 2022))."""
    with ApiClient():
        chs_district = District("chs", 2022)
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
