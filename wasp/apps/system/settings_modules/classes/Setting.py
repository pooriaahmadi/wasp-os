from .Field import Field


class Setting:
    NAME = ""
    ORDER = 0

    def __init__(self) -> None:
        self.fields: list[Field] = []

    def register_field(self, field: Field):
        self.fields.append(field)

    def remove_field(self, name: str):
        for field in self.fields:
            if field.name == name:
                self.fields.remove(field)
                break

    def retrieve_field_values(self):
        for field in self.fields:
            field.get()

    def _draw(self):
        # draw the page
        pass

    def update(self):
        pass

    def touch(self, event):
        pass
