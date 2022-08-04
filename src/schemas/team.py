from .base_schema import BaseSchema


class Team(BaseSchema):
    """Class represening a team's metadata with methods to get team specific data."""

    def __eq__(self, other) -> bool:
        return self.team_number == other.team_number

    def __hash__(self) -> int:
        return self.team_number

    def __lt__(self, other: "Team") -> bool:
        return self.team_number < other.team_number
