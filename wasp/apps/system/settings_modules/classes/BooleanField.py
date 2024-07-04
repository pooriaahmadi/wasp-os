from .Field import Field


class BooleanField(Field):

    def __init__(self, name: str, default: bool, setting_name: str) -> None:
        super().__init__(name, default, setting_name)
