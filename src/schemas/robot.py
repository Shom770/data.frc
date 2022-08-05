from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class Robot(BaseSchema):
    """Class representing a robot containing methods to get specific district information."""
