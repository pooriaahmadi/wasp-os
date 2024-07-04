from .classes import Setting, IntField
import wasp
import fonts


class RaiseToWake(Setting):
    NAME = "Raise To Wake"
    ORDER = 5

    def __init__(self) -> None:
        super().__init__()
        self.register_field(IntField("state", 0, RaiseToWake.NAME))
        self._raise_to_wake_toggle = wasp.widgets.ToggleButton(
            32, 90, 176, 48, "On/Off"
        )

    def retrieve_field_values(self):
        super().retrieve_field_values()
        self._raise_to_wake_toggle.state = True if self.fields[0].value == 1 else False

    def touch(self, event):
        if self._raise_to_wake_toggle.touch(event):
            wasp.system.raise_wake = 1 if wasp.system.raise_wake == 0 else 0

        self.update()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Raise To Wake", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable

        self._raise_to_wake_toggle.draw()
        draw.reset()
        if wasp.system.raise_wake:
            say = "On"
        else:
            say = "Off"
        draw.string(say, 0, 150, width=240)
