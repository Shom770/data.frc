from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class District(BaseSchema):
    """Class representing a district containing methods to get specific district information."""
