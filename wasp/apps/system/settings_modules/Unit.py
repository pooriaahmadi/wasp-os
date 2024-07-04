from .classes import Setting, IntField
import wasp
import fonts


class Unit(Setting):
    NAME = "Unit"
    ORDER = 4

    def __init__(self) -> None:
        super().__init__()
        self.register_field(IntField("index", 0, Unit.NAME))
        self._units_toggle = wasp.widgets.Button(32, 90, 176, 48, "Change")
        self._units = ["Metric", "Imperial"]

    def retrieve_field_values(self):
        super().retrieve_field_values()
        wasp.system.units = self._units[self.fields[0].value % len(self._units)]

    def update_index(self, new_value):
        self.fields[0].value = new_value
        wasp.system.units = self._units[new_value % len(self._units)]

    def touch(self, event):
        if self._units_toggle.touch(event):
            self.update_index(self._units.index(wasp.system.units) + 1)

        self.update()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Unit", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable

        self._units_toggle.draw()
        draw.reset()
        draw.string(wasp.system.units, 0, 150, width=240)
