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

    @dataclass(repr=True)
    class Record:
        """Class representing a record of wins, losses and ties for qualification matches, playoffs, and more."""

        losses: int
        ties: int
        wins: int

    def __init__(self, event_key: str, team_status_info: dict):
        self.event_key = event_key
        self.alliance = self.Alliance(**team_status_info["alliance"])
        self.alliance_status_str = team_status_info["alliance_status_str"]
        self.last_match_key = team_status_info["last_match_key"]
        self.next_match_key = team_status_info["next_match_key"]
        self.overall_status_str = team_status_info["overall_status_str"]

