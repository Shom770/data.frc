class BaseSchema:
    """Base class for all schemas."""

    _headers = None

    def __init__(self, attrs: dict):
        self._attributes_formatted = ", ".join(
            [f"{attr_name}={attr_value}" for attr_name, attr_value in attrs.items()]
        ).rstrip(", ")

    def __repr__(self):
        return f"{type(self).__name__}({self._attributes_formatted})"

    @classmethod
    def add_headers(cls, headers: dict) -> None:
        """
        Adds headers for subclasses' uses when sending requests (GET/POST).

        Parameters:
            headers: A dictionary that is in the format of {"X-TBA-Auth-Key": api_key} for TBA be able to authorize sending requests.
        """
        cls._headers = headers
