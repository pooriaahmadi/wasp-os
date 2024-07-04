from .Field import Field


class IntField(Field):

    def __init__(self, name: str, default: int, setting_name: str) -> None:
        super().__init__(name, default, setting_name)
