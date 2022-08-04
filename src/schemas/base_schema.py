class BaseSchema:
    """Base class for all schemas."""

    def __init__(self, parent_api_client: "ApiClient", **kwargs):
        attributes_formatted = ""

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
            attributes_formatted += f"{attr_name}={attr_value}, "

        self._attributes_formatted = attributes_formatted.rstrip(", ")
        self._parent_api_client = parent_api_client

    def __repr__(self):
        return f"{type(self).__name__}({self._attributes_formatted})"
