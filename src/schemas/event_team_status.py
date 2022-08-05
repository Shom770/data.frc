import typing
from dataclasses import dataclass


class EventTeamStatus:
    """Class representing a team's status during an event."""

    @dataclass(repr=True)
    class Alliance:
        """Class representing the alliance said team was on during an event."""

        backup: typing.Union[dict, None]
        name: str
        number: int
        pick: int

    def __init__(self, event_key: str, team_status_info: dict):
        self.event_key = event_key
        self.alliance = self.Alliance(**team_status_info["alliance"])
