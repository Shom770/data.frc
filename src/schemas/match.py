import typing

from .base_schema import BaseSchema
from .district import District
from .event import Event
from .event_team_status import EventTeamStatus
from .robot import Robot

try:
    from utils import *
except ImportError:
    from ..utils import *


class Match(BaseSchema):
    """Class representing a match's metadata with methods to get match specific data."""
