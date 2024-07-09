# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020-21 Daniel Thompson

"""Settings application
~~~~~~~~~~~~~~~~~~~~~~~

Allows a very small set of user preferences (including the date and
time) to be set on the device itself.

.. figure:: res/screenshots/SettingsApp.png
    :width: 179

.. note::

    The settings tool is not expected to comprehensively present every
    user configurable preference. Some are better presented via a
    companion app and some particular exotic ones are perhaps best
    managed with a user-provided ``main.py``.
"""


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
        self._slider = None
        self._nfy_slider = None
        self._HH = None
        self._MM = None
        self._dd = None
        self._mm = None
        self._yy = None
        self._units = None
        self._units_toggle = None
        self._settings = None
        self._sett_index = None
        self.current_page = None

    def foreground(self):
        self._slider = wasp.widgets.Slider(3, 10, 90)
        self._nfy_slider = wasp.widgets.Slider(3, 10, 90)
        self._HH = wasp.widgets.Spinner(50, 60, 0, 23, 2)
        self._MM = wasp.widgets.Spinner(130, 60, 0, 59, 2)
        self._dd = wasp.widgets.Spinner(20, 60, 1, 31, 1)
        self._mm = wasp.widgets.Spinner(90, 60, 1, 12, 1)
        self._yy = wasp.widgets.Spinner(160, 60, 20, 60, 2)
        self._units = ["Metric", "Imperial"]
        self._units_toggle = wasp.widgets.Button(32, 90, 176, 48, "Change")
        self._settings = ["Brightness", "Notification Level", "Time", "Date", "Units"]
        self._sett_index = -1
        self.current_page = 0

        self._slider.value = wasp.system.brightness - 1
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH)
        wasp.system.request_event(
            wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT
        )

    # def background(self):
    # self._slider = None
    # del self._slider
    # self._nfy_slider = None
    # del self._nfy_slider
    # self._HH = None
    # del self._HH
    # self._MM = None
    # del self._MM
    # self._dd = None
    # del self._dd
    # self._mm = None
    # del self._mm
    # self._yy = None
    # del self._yy
    # self._units = None
    # del self._units
    # self._units_toggle = None
    # del self._units_toggle
    # self._settings = None
    # del self._settings
    # self._sett_index = None
    # del self._sett_index
    # self.current_page = None
    # del self.current_page

    # wasp.gc.collect()

    def touch(self, event):
        if self._sett_index == -1:
            self._sett_index = int(
                (event[2] // (240 / SETTINGS_PER_PAGE))
                + (self.current_page * SETTINGS_PER_PAGE)
            )
            self._draw()
        elif self._sett_index == 0:
            self._slider.touch(event)
            wasp.system.brightness = self._slider.value + 1
        elif self._sett_index == 1:
            self._nfy_slider.touch(event)
            wasp.system.notify_level = self._nfy_slider.value + 1
        elif self._sett_index == 2:
            if self._HH.touch(event) or self._MM.touch(event):
                now = list(wasp.watch.rtc.get_localtime())
                now[3] = self._HH.value
                now[4] = self._MM.value
                wasp.watch.rtc.set_localtime(now)
        elif self._sett_index == 3:
            if self._yy.touch(event) or self._mm.touch(event) or self._dd.touch(event):
                now = list(wasp.watch.rtc.get_localtime())
                now[0] = self._yy.value + 2000
                now[1] = self._mm.value
                now[2] = self._dd.value
                wasp.watch.rtc.set_localtime(now)
        elif self._sett_index == 4:
            if self._units_toggle.touch(event):
                wasp.system.units = self._units[
                    (self._units.index(wasp.system.units) + 1) % len(self._units)
                ]
        self._update()

    def swipe(self, event):
        """Handle NEXT events by augmenting the default processing by resetting
        the count if we are not currently timing something.

        No other swipe event is possible for this application.
        """
        if self._sett_index >= 0:
            if event[0] == wasp.EventType.RIGHT or event[0] == wasp.EventType.LEFT:
                self.current_page = 0
                self._sett_index = -1
                self._draw()
            return

        if event[0] == wasp.EventType.UP:
            if self.current_page + 2 > len(self._settings) // SETTINGS_PER_PAGE:
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

    def draw_page(self):
        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_font(fonts.sans18)

        draw.set_color(
            wasp.system.theme("bright"), draw.darken(wasp.system.theme("mid"), 17)
        )
        end_limit = self.current_page * SETTINGS_PER_PAGE + 5
        if end_limit > len(self._settings):
            end_limit = len(self._settings)

        for i in range(self.current_page * SETTINGS_PER_PAGE, end_limit):
            draw.fill(
                x=0, y=48 * (i - self.current_page * SETTINGS_PER_PAGE), w=240, h=45
            )
            draw.string(
                self._settings[i],
                20,
                (48 * (i - self.current_page * SETTINGS_PER_PAGE)) + 15,
            )

    def _draw(self):
        """Redraw the display from scratch."""

        if self._sett_index == -1:
            self.draw_page()
            return

        draw = wasp.watch.drawable
        draw.reset()
        draw.fill()
        draw.set_color(wasp.system.theme("bright"))
        draw.set_font(fonts.sans24)
        draw.string(self._settings[self._sett_index], 0, 6, width=240)
        if self._sett_index == 0:
            self._slider.value = wasp.system.brightness - 1
        elif self._sett_index == 1:
            self._nfy_slider.value = wasp.system.notify_level - 1
        elif self._sett_index == 2:
            now = wasp.watch.rtc.get_localtime()
            self._HH.value = now[3]
            self._MM.value = now[4]
            draw.set_font(fonts.sans28)
            draw.string(":", 110, 120 - 14, width=20)
            self._HH.draw()
            self._MM.draw()
        elif self._sett_index == 3:
            now = wasp.watch.rtc.get_localtime()
            self._yy.value = now[0] - 2000
            self._mm.value = now[1]
            self._dd.value = now[2]
            self._yy.draw()
            self._mm.draw()
            self._dd.draw()
            draw.set_font(fonts.sans24)
            draw.string("DD    MM    YY", 0, 180, width=240)
        elif self._sett_index == 4:
            self._units_toggle.draw()

        self._update()

    def _update(self):
        draw = wasp.watch.drawable
        draw.set_color(wasp.system.theme("bright"))
        if self._sett_index == 0:
            if wasp.system.brightness == 3:
                say = "High"
            elif wasp.system.brightness == 2:
                say = "Mid"
            else:
                say = "Low"
            self._slider.update()
            draw.string(say, 0, 150, width=240)
        elif self._sett_index == 1:
            if wasp.system.notify_level == 3:
                say = "High"
            elif wasp.system.notify_level == 2:
                say = "Mid"
            else:
                say = "Silent"
            self._nfy_slider.update()
            draw.string(say, 0, 150, width=240)
        elif self._sett_index == 4:
            draw.string(wasp.system.units, 0, 150, width=240)
