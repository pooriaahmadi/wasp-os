from .classes import Setting, IntField
import wasp
import fonts


class Notification(Setting):
    NAME = "Notification Level"
    ORDER = 1

    def __init__(self) -> None:
        super().__init__()

        self.register_field(
            IntField("level", default=2, setting_name=Notification.NAME)
        )
        self._nfy_slider = wasp.widgets.Slider(3, 10, 90)

    def retrieve_field_values(self):
        super().retrieve_field_values()
        self._nfy_slider.value = self.fields[0].value - 1

    def touch(self, event):
        self._nfy_slider.touch(event)
        wasp.system.notify_level = self._nfy_slider.value + 1
        self.update()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Notification Level", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable
        self._nfy_slider.value = wasp.system.notify_level - 1
        if wasp.system.notify_level == 3:
            say = "High"
        elif wasp.system.notify_level == 2:
            say = "Mid"
        else:
            say = "Silent"
        self._nfy_slider.update()
        draw.string(say, 0, 150, width=240)
