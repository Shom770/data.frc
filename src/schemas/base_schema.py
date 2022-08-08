class BaseSchema:
    """Base class for all schemas."""

    _headers = None

    def __init__(self):
        attributes_formatted = ""

        for attr_name, attr_value in vars(self).items():
            if isinstance(attr_value, dict):
                attributes_formatted += f"{attr_name}={{...}}, "
            elif isinstance(attr_value, list):
                attributes_formatted += f"{attr_name}=[...], "
            elif type(attr_value).__qualname__.startswith("schemas"):
                attributes_formatted += f"{attr_name}={type(attr_value).__name__}(...), "
            else:
                attributes_formatted += f"{attr_name}={attr_value!r}, "

        self._attributes_formatted = attributes_formatted[:-2]

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
