import typing
from dataclasses import dataclass
from enum import Enum


class EventTeamStatus:
    """Class representing a team's status during an event."""

    class Status(Enum):
        """Enum class representing the status of the team during an event"""

        WON = 1
        ELIMINATED = 2
        PLAYING = 3

    @dataclass()
    class SortOrders:
        """Information about the team used to determine ranking for an event."""

        def __init__(self, sort_orders: list, sort_order_info: list[dict]):
            for data, data_info in zip(sort_orders, sort_order_info):
                setattr(self, data_info["name"].lower().replace(" ", "_"), data)

    @dataclass()
    class Ranking:
        """Class representing a team's ranking information during qualifications of an event."""

        dq: int
        matches_played: int
        qual_average: typing.Optional[float]
        rank: int
        record: "EventTeamStatus.Record"
        sort_orders: "EventTeamStatus.SortOrders"

    @dataclass()
    class Alliance:
        """Class representing the alliance said team was on during an event."""

        backup: typing.Optional[dict]
        name: str
        number: int
        pick: int

    @dataclass()
    class Record:
        """Class representing a record of wins, losses and ties for qualification matches, playoffs, and more."""

        losses: int
        ties: int
        wins: int

    @dataclass()
    class Playoff:
        """Class representing the team's performance during playoffs."""

        current_level_record: "EventTeamStatus.Record"
        level: str
        playoff_average: typing.Optional[int]
        record: "EventTeamStatus.Record"
        status: "EventTeamStatus.Status"

    @dataclass()
    class Qualifications:
        """Class representing the team's performance during qualifications."""

        num_teams: int
        ranking: "EventTeamStatus.Ranking"
        status: "EventTeamStatus.Status"

    def __init__(self, event_key: str, team_status_info: dict):
        self.event_key = event_key

        if team_status_info["alliance"]:
            self.alliance = self.Alliance(**team_status_info["alliance"])
        else:
            self.alliance = None

        self.alliance_status_str = team_status_info["alliance_status_str"]
        self.last_match_key = team_status_info["last_match_key"]
        self.next_match_key = team_status_info["next_match_key"]
        self.overall_status_str = team_status_info["overall_status_str"]

        if team_status_info["playoff"]:
            self.playoff = self.Playoff(
                current_level_record=self.Record(**team_status_info["playoff"]["current_level_record"]),
                level=team_status_info["playoff"]["level"],
                playoff_average=team_status_info["playoff"]["playoff_average"],
                record=self.Record(**team_status_info["playoff"]["record"]),
                status=getattr(self.Status, team_status_info["playoff"]["status"].upper())
            )
        else:
            self.playoff = None

        self.playoff_status_str = team_status_info["playoff_status_str"]
