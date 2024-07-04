from .classes import Setting
import wasp
import fonts


class Date(Setting):
    NAME = "Date"
    ORDER = 3

    def __init__(self) -> None:
        super().__init__()
        self._dd = wasp.widgets.Spinner(20, 60, 1, 31, 1)
        self._mm = wasp.widgets.Spinner(90, 60, 1, 12, 1)
        self._yy = wasp.widgets.Spinner(160, 60, 20, 60, 2)

    def _draw(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string("Current Date", 0, 6, width=240)
        self.update()

    def update(self):
        draw = wasp.watch.drawable

        now = wasp.watch.rtc.get_localtime()
        self._yy.value = now[0] - 2000
        self._mm.value = now[1]
        self._dd.value = now[2]
        self._yy.draw()
        self._mm.draw()
        self._dd.draw()
        draw.set_font(fonts.sans24)
        draw.string("DD    MM    YY", 0, 180, width=240)

    def touch(self, event):
        if self._yy.touch(event) or self._mm.touch(event) or self._dd.touch(event):
            now = list(wasp.watch.rtc.get_localtime())
            now[0] = self._yy.value + 2000
            now[1] = self._mm.value
            now[2] = self._dd.value
            wasp.watch.rtc.set_localtime(now)

        self.update()
