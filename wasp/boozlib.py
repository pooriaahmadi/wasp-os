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
