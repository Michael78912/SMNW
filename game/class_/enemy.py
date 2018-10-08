class Enemy:
    """base class for stickmanranger enemies"""

    def __init__(self, stats, colour):
        if not type(stats) in [tuple, list, set]:
            raise TypeError(
                'stats must be a sequence of ints. which %a is not, unfortunately :('
                % stats)

        self.stats = stats
        self.stats = stats[0]

        if type(colour) == str:
            import dicts
