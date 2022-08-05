from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class District(BaseSchema):
    """Class representing a district's method containing methods to get specific district information."""
