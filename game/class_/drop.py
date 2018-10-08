"""
drop.py
this is a base class, that is to derive compos/weapons from (and anything i might add later ;))
definitely not to be used directly.
"""


class DropItem:
    def __init__(self, smallicon, largeicon, surface, stats_to_display=''):
        self.smallicon = smallicon
        self.largeicon = largeicon
        if isinstance(stats_to_display, dict):
            self.stats_to_display = stats_to_display

        elif isinstance(stats_to_display, str):
            d = stats_to_display.split('\n')
            stats_to_display = {}
            for i in d:
                stats_to_display[i.split(':')[0]] = i.split(':')[1]
            self.stats_to_display = stats_to_display

    def draw_large(self, pos):
        """
        blits self.largeicon to surface.
        """
        self.surface.blit(self.largeicon, pos)

    def draw_small(self, pos):
        self.surface.blit(self.smallicon, pos)
