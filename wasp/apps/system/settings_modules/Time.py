from .classes import Setting
import wasp
import fonts


class Time(Setting):
    NAME = "Time"
    ORDER = 2

    def __init__(self) -> None:
        super().__init__()
        self._HH = wasp.widgets.Spinner(50, 60, 0, 23, 2)
        self._MM = wasp.widgets.Spinner(130, 60, 0, 59, 2)

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Current Time", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable

        now = wasp.watch.rtc.get_localtime()
        self._HH.value = now[3]
        self._MM.value = now[4]
        draw.set_font(fonts.sans28)
        draw.string(":", 110, 120 - 14, width=20)
        self._HH.draw()
        self._MM.draw()

    def touch(self, event):
        if self._HH.touch(event) or self._MM.touch(event):
            now = list(wasp.watch.rtc.get_localtime())
            now[3] = self._HH.value
            now[4] = self._MM.value
            wasp.watch.rtc.set_localtime(now)

        self.update()
