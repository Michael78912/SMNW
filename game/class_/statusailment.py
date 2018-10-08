try:
    from _internal import *

except ImportError:
    from ._internal import *


class StatusAilment:
    def __init__(self, colour):
        self.colour = colour
