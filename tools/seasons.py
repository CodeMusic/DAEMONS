"""T-359 / companion C-14: the seasons, defined once (vision 9.21). A library -- nothing runs on import -- read by
tools/companion_export.py (the companion's seasons.json) and, when T-359 is built, by the game's own table.

CONTENT keeps the northern year and CONTEXT the southern (the user, 2026-10-03): from December 21 to March 20 it is
winter in CONTENT and summer in CONTEXT. A season begins on its date and runs to the day before the next one."""

SEASONS = ("winter", "spring", "summer", "autumn")

# The northern year: (month, day) each season begins, in the order winter, spring, summer, autumn.
NORTH_STARTS = {"winter": (12, 21), "spring": (3, 21), "summer": (6, 21), "autumn": (9, 22)}

# Which hemisphere each edition keeps.
EDITION_HEMISPHERE = {"CONTENT": "north", "CONTEXT": "south"}

# Without a clock the game counts play time instead (vision 9.21's proposal): a season every seven days of play,
# and a day of play is an hour (T-273), so a season is seven hours of play.
PLAY_HOURS_PER_SEASON = 7


def north_season(month, day):
    """The northern season on a calendar date."""
    md = (month, day)
    if md >= NORTH_STARTS["winter"] or md < NORTH_STARTS["spring"]:
        return "winter"
    if md < NORTH_STARTS["summer"]:
        return "spring"
    if md < NORTH_STARTS["autumn"]:
        return "summer"
    return "autumn"


def season(edition, month, day):
    """The season an edition keeps on a date: the southern year is the northern one, two seasons on."""
    s = north_season(month, day)
    if EDITION_HEMISPHERE[edition] == "south":
        s = SEASONS[(SEASONS.index(s) + 2) % 4]
    return s
