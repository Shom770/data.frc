import pytest

from ..api_client import ApiClient
from ..schemas import *
from ..utils import *


def test_district_year_abbreviation():
    """Tests initializing `District` via passing in the year and then the abbreviation (eg District(2022, 'chs'))"""
    with ApiClient():
        chs_district = District(2022, "chs")
        assert chs_district.year == 2022 and chs_district.abbreviation == "chs" and chs_district.key == "2022chs"
