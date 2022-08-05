from utils.internal_data import InternalData


class BaseSchema:
    """Base class for all schemas."""

    def __init_subclass__(cls):
        cls._internal_data = InternalData

    def __init__(self, **kwargs):
        attributes_formatted = ""

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
            attributes_formatted += f"{attr_name}={attr_value}, "

        self._attributes_formatted = attributes_formatted.rstrip(", ")

    def __repr__(self):
        return f"{type(self).__name__}({self._attributes_formatted})"
