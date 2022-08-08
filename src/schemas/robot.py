from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class Robot(BaseSchema):
    """Class representing a robot containing methods to get specific district information."""

    def __init__(self, **kwargs):
        self.year: int = kwargs["year"]
        self.robot_name: str = kwargs["robot_name"]
        self.key: str = kwargs["key"]
        self.team_key: str = kwargs["team_key"]

        super().__init__(kwargs)
