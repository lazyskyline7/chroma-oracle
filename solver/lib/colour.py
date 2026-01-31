"""Colours for use in the game."""

from enum import Enum

from sty import fg

LI_GREEN = fg(153, 255, 153)
LI_BLUE = fg(102, 255, 255)
GREEN = fg(102, 153, 0)
BROWN = fg(110, 79, 43)
ORANGE = fg(255, 150, 50)
PINK = fg(255, 153, 204)


class Colour(Enum):
    """Colours that can be used."""

    RED = fg.red
    PINK = PINK
    BROWN = BROWN
    GREEN = GREEN
    LIGHT_GREEN = LI_GREEN
    DARK_GREEN = fg.da_green
    YELLOW = fg.yellow
    BLUE = fg.blue
    LIGHT_BLUE = LI_BLUE
    DARK_BLUE = fg.da_blue
    GREY = fg(245)
    PURPLE = fg(93)
    ORANGE = ORANGE
    UNKNOWN = fg.black
