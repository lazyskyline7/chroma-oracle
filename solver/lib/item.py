"""Module representing a single coloured item."""

from solver.lib.colour import Colour


class Item:
    """A representation of a coloured thing that is comparable."""

    def __init__(self, colour: Colour | str):
        """Create a new coloured thing."""
        if isinstance(colour, Colour):
            self.colour = colour
        if isinstance(colour, str):
            if colour == "?":
                self.colour = Colour.UNKNOWN
            elif colour in Colour.__members__:
                self.colour = Colour[colour]
            else:
                self.colour = Colour(colour)

    def __eq__(self, other):
        """Check if this item's colour matches other."""
        if isinstance(other, Item):
            return self.colour == other.colour
        if isinstance(other, Colour):
            return self.colour == other
        if isinstance(other, str):
            if other in Colour.__members__:
                return self.colour == Colour[other]
            return self.colour == Colour(other)
        return False

    def __ne__(self, other):
        """Check if this item's colour is different to another."""
        return not self.__eq__(other)

    def __str__(self):
        """Get a square of `colour` for printing."""
        return self.colour.value + "\u25a0\x1b[39m"

    def __repr__(self):
        """Get the colour's name."""
        return f"'{self.colour.name}'"

    def __hash__(self):
        """Get the hash of the colour of this item."""
        return hash(self.colour)
