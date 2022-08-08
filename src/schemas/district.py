import typing

from .base_schema import BaseSchema

try:
    from utils import *
except ImportError:
    from ..utils import *


class District(BaseSchema):
    """Class representing a district containing methods to get specific district information."""

    def __init__(self, **kwargs):
        self.abbreviation: typing.Optional[str] = kwargs.get("abbreviation")
        self.display_name: typing.Optional[str] = kwargs.get("display_name")
        self.key: str = kwargs["key"]
        self.year: typing.Optional[int] = kwargs.get("year")

        super().__init__(kwargs)
