from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class Event(BaseSchema):
    """Class representing an event containing methods to get specific event information."""
