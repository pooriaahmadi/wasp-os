import wasp
import icons
import fonts
import array
import time

from micropython import const

ALCOHOL_DENSITY = const(0.8)  #: density of alcohol (g/ml)
BLOOD_DENSITY = const(1.055)  #: density of blood (g/ml)
WATER_IN_BLOOD = const(0.8)  #: parts of water in blood (%)
ALCOHOL_DEGRADATION = const(0.0025)  #: for kg body weight per minute (g)


def calculate_alcohol_weight(volume, percent):
    return ALCOHOL_DENSITY * volume * (percent / 100)


def calculate_alcohol_degradation(weight, minutes=1):
    return ALCOHOL_DEGRADATION * weight * minutes


def calculate_body_water(age, weight, height, sex):
    if sex:  # female
        return 0.203 - (0.07 * age) + (0.1069 * height) + (0.2466 * weight)
    else:  # male
        return 2.447 - (0.09516 * age) + (0.1074 * height) + (0.3362 * weight)


def promille_to_gramm(promille, body_water):
    return (promille * (BLOOD_DENSITY * body_water)) / WATER_IN_BLOOD


def gramm_to_promille(gramm, body_water):
    return (gramm * WATER_IN_BLOOD) / (BLOOD_DENSITY * body_water)


def get_blood_alcohol_content(
    age,
    weight,
    height,
    sex,
    volume,
    percent,
):
    gramm = calculate_alcohol_weight(volume=volume, percent=percent)
    body_water = calculate_body_water(age=age, weight=weight, height=height, sex=sex)
    return gramm_to_promille(gramm=gramm, body_water=body_water)


def get_blood_alcohol_degradation(
    age,
    weight,
    height,
    sex,
    minutes=1,
) -> float:
    gramm = calculate_alcohol_degradation(weight=weight, minutes=minutes)
    body_water = calculate_body_water(age=age, weight=weight, height=height, sex=sex)
    return gramm_to_promille(gramm=gramm, body_water=body_water)


def bac_time(age, weight, height, sex, minutes, volume, percent):
    return max(
        0,
        (
            get_blood_alcohol_content(age, weight, height, sex, volume, percent)
            - get_blood_alcohol_degradation(age, weight, height, sex, minutes)
        )
        / 10,
    )


def string_to_time(time_str):
    date, t = time_str.split()
    year, month, day = map(int, date.split("-"))
    hour, minute = map(int, t.split(":"))
    return time.mktime((year, month, day, hour, minute, 0, 0, 0, 0))


def minutes_passed(time_str):
    past_time = string_to_time(time_str)
    current_time = time.time()
    time_difference = current_time - past_time
    minutes = int(time_difference / 60)
    return minutes


class WineApp(object):

    NAME = "Wine"
    ICON = icons.wine

    def __init__(self) -> None:
        self._drinks = array.array("B", [0, 0, 0])
        try:
            with open("drinks.txt", "r", encoding="utf-8") as f:
                last_line = f.readlines()[-1]
                if "\n" in last_line:
                    last_line = ""
            for drink in last_line.split(";"):
                try:
                    self._drinks[int(drink.split(",")[0])] += 1
                except:
                    pass
        except OSError:
            with open("drinks.txt", "w", encoding="utf-8") as f:
                pass

    def foreground(self):
        """Activate the application."""
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_LEFTRIGHT)
        self._page = 0
        self._spinner = wasp.widgets.Spinner(90, 100, 0, 10)
        self.end_session = wasp.widgets.Button(10, 150, 220, 80, "END")
        self._draw()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill(0)
        sbar = wasp.system.bar
        sbar.clock = True
        sbar.draw()
        draw.set_font(fonts.sans24)

        if self._page == 3:
            draw.string("Sober?", 0, 50, width=240)
            with open("drinks.txt", "r", encoding="utf-8") as f:
                last_line = f.readlines()[-1]
                if "\n" in last_line:
                    last_line = ""

            _BAC = 0
            for drink_txt in last_line.split(";"):
                if len(drink_txt) < 5:
                    continue
                drink_type, date = drink_txt.split(",")
                alcohol_percentage = 0
                amount = 0
                if drink_type == "0":
                    alcohol_percentage = 15
                    amount = 250
                elif drink_type == "1":
                    alcohol_percentage = 5
                    amount = 355
                elif drink_type == "2":
                    alcohol_percentage = 40
                    amount = 30

                _BAC += bac_time(
                    19, 70, 168, False, minutes_passed(date), amount, alcohol_percentage
                )

            draw.string("BAC: " + str(round(_BAC, 3)) + "%", 0, 100, width=240)
            return

        if self._page == 4:
            draw.string("End session?", 0, 50, width=240)
            self.end_session.draw()
            return

        if self._page == 0:
            draw.string("Wine", 0, 50, width=240)
        elif self._page == 1:
            draw.string("Beer", 0, 50, width=240)
        elif self._page == 2:
            draw.string("Vodka", 0, 50, width=240)

        self._spinner.value = self._drinks[self._page]
        self._spinner.draw()

    def background(self):
        """De-activate the application (without losing original state)."""
        self._spinner = None
        del self._spinner
        self._page = None
        del self._page
        self.end_session = None
        del self.end_session

    def tick(self, ticks):
        wasp.system.keep_awake()

    def swipe(self, event):
        if event[0] == wasp.EventType.LEFT:
            self._page += 1
            if self._page > 4:
                self._page = 0
        elif event[0] == wasp.EventType.RIGHT:
            self._page -= 1
            if self._page < 0:
                self._page = 4

        self._draw()

    def touch(self, event):
        if self._page == 4:
            if self.end_session.touch(event):
                if sum(self._drinks) == 0:
                    return
                with open("drinks.txt", "a", encoding="utf-8") as f:
                    f.write("\n")
                for i in range(len(self._drinks)):
                    self._drinks[i] = 0
                wasp.system.navigate(wasp.EventType.HOME)
        else:
            self._spinner.touch(event)
            if self._drinks[self._page] < self._spinner.value:
                with open("drinks.txt", "a", encoding="utf-8") as f:
                    f.write(
                        str(self._page)
                        + ","
                        + time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
                        + ";"
                    )
            self._drinks[self._page] = self._spinner.value
