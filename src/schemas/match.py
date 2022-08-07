import typing
from dataclasses import dataclass

from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class Match(BaseSchema):
    """Class representing a match's metadata with methods to get match specific data."""

    @dataclass()
    class Alliance:
        """Class representing an alliance's performance/metadata during a match."""

        score: typing.Optional[int]
        team_keys: list[str]
        surrogate_team_keys: list[str]
        dq_team_keys: list[str]
