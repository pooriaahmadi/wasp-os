import wasp
import fonts
import icons
from micropython import const


SETTINGS_PER_PAGE = const(5)


class SettingsApp:
    """Settings application."""

    NAME = "Settings"
    ICON = icons.settings

    def __init__(self) -> None:
        self.current_page = 0
        self.backup_current_page = None

    def background(self):
        self.current_page = 0
        self.backup_current_page = None

    def foreground(self):
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH)
        wasp.system.request_event(wasp.EventMask.SWIPE_UPDOWN)
        wasp.system.request_event(wasp.EventMask.SWIPE_LEFTRIGHT)

    def draw_page(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_font(fonts.sans18)

        draw.set_color(
            wasp.system.theme("bright"), draw.darken(wasp.system.theme("mid"), 17)
        )
        end_limit = self.current_page * SETTINGS_PER_PAGE + 5
        if end_limit > len(wasp.system.setting_classes):
            end_limit = len(wasp.system.setting_classes)

        for i in range(self.current_page * SETTINGS_PER_PAGE, end_limit):
            draw.fill(
                x=0, y=48 * (i - self.current_page * SETTINGS_PER_PAGE), w=240, h=45
            )
            draw.string(
                wasp.system.setting_classes[i].NAME,
                20,
                (48 * (i - self.current_page * SETTINGS_PER_PAGE)) + 15,
            )

    def touch(self, event):
        if isinstance(self.current_page, str):
            self.get_current_class().touch(event)
        else:
            self.backup_current_page = self.current_page
            self.current_page = wasp.system.setting_classes[
                int(
                    (event[2] // (240 / SETTINGS_PER_PAGE))
                    + (self.current_page * SETTINGS_PER_PAGE)
                )
            ].NAME
            self._draw()

    def swipe(self, event):
        if isinstance(self.current_page, str):
            if event[0] == wasp.EventType.RIGHT or event[0] == wasp.EventType.LEFT:
                self.current_page = self.backup_current_page
                self.backup_current_page = None
                self._draw()
            return

        if event[0] == wasp.EventType.UP:

            if (
                self.current_page + 1
                > len(wasp.system.setting_classes) // SETTINGS_PER_PAGE
            ):
                wasp.watch.vibrator.pulse()
            else:
                self.current_page += 1
                self._draw()
        elif event[0] == wasp.EventType.DOWN:
            if self.current_page - 1 < 0:
                wasp.watch.vibrator.pulse()
            else:
                self.current_page -= 1
                self._draw()

    def get_current_class(self):
        for setting_class in wasp.system.setting_classes:
            if setting_class.NAME == self.current_page:
                return setting_class

    def _draw(self):
        if isinstance(self.current_page, str):
            self.get_current_class()._draw()
        else:
            self.draw_page()

    def _update(self):
        pass
