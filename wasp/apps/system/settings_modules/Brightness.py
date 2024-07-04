from .classes import Setting, IntField
import watch
import wasp
import fonts


class Brightness(Setting):
    NAME = "Brightness"
    ORDER = 0

    def __init__(self) -> None:
        super().__init__()
        self.register_field(IntField("level", default=2, setting_name=Brightness.NAME))
        self._slider = wasp.widgets.Slider(3, 10, 90)

    def retrieve_field_values(self):
        super().retrieve_field_values()
        watch.backlight.set(self.fields[0].value)
        self._slider.value = self.fields[0].value - 1

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Brightness", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable

        self._slider.value = self.fields[0].value - 1

        if wasp.system.brightness == 3:
            say = "High"
        elif wasp.system.brightness == 2:
            say = "Mid"
        else:
            say = "Low"
        self._slider.update()
        draw.string(say, 0, 150, width=240)

    def touch(self, event):
        self._slider.touch(event)
        wasp.system.brightness = self._slider.value + 1
        self.update()
