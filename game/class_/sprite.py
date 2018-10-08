"""
this is the base class for basically anything
that moves in this game.
"""
__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0'

from queue import Queue
import pprint
import threading

import pygame as pg

try:
    from events import Quit, SayHello
    from terrain import Terrain

except ImportError:
    from .events import Quit, SayHello
    from .terrain import Terrain


class SMRSprite:
    sizey = 0
    sizex = 0
    """
    this is the base class for everything that can move 
    in this game. enemies, attacks, weapons, and projectiles.
    _mainloop does nothing in this base class, it is just there
    because it is called by start_thread.
    """

    def __init__(self, main_game_state, event_queue, pos):
        self.main_game_state = main_game_state
        self.event_queue = event_queue
        self._internal_events = Queue()

        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def internal_event(self, ev):
        self._internal_events.put(ev)

    @staticmethod
    def find_closest_of(terrain, block, x=0):
        """
        finds the first solid part of terrain, and returns the
        index as a tuple.
        """

        terrain2d = terrain.terrain2dlist_texts[terrain.template]['text']
        if terrain.use_numpy:
            line = terrain2d[:, x]

        else:
            line = [i[0] for i in terrain2d]
        # print(line)

        for iblock, index in zip(line, range(len(line))):
            # this is going the correct way, I believe
            # print(line, block)
            if iblock == block:
                return x, index

        else:
            raise TypeError('there are no %a symbols in %a' % (block, line))

    @classmethod
    def get_topleft_coord(cls, terrain, x, y):
        """
        returns the correct coordinate 
        from terrain, in pixels, rather than blocks.
        """
        template = terrain.terrain2dlist_texts[terrain.template]
        blk_size = template['size']
        x_line_size_pixels = len(
            template['text'][:, x]) * blk_size if terrain.use_numpy else len(
                [i[0] for i in template['text']]) * blk_size
        y_line_size_pixels = len(template['text'][0]) * blk_size
        new_x = x * blk_size
        new_y = y * blk_size
        assert new_x < x_line_size_pixels and new_y < y_line_size_pixels, 'the coordinate is too big for the screen'
        return (new_x - cls.sizex, new_y - cls.sizey)
        # this is all correct so far

    def update_coords(self, pos):
        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def game_quit(self):
        """
        request a quit from the actual game, if needed.
        """

        self.event_queue.put(Quit())

    def kill_thread(self):
        """
        attempts to kill the current thread, with 
        cleanup (removes character from screen, etc...)
        """
        self._internal_events.put(Quit())

    def start_thread(self, daemon=True):
        """
        starts a new thread and redirects it to _mainloop.
        daemon is default to true.
        """
        self.mainthread = threading.Thread(
            target=self._mainloop, daemon=daemon)
        self.mainthread.start()

    def _mainloop(self):
        while 1:
            if self._internal_events.empty():
                pass
            else:
                self._internal_events.get()()

            # used for debugging
            print(threading.current_thread())


if __name__ == '__main__':
    d = Terrain('dirt', 'test', use_numpy=True)
    # print([i.tolist() for i in d.terrain2dlist_texts['test']['text']])
    s1, s2 = SMRSprite.find_closest_of(d, '#')
    print(s1, s2)

    # print(s1, s2)
    # s = repr(list([list(i) for i in d.terrain2dlist_texts[d.template]['text']]))
    # a = list([list(i) for i in d.terrain2dlist_texts[d.template]['text']])
    # print(a)
    print(SMRSprite.get_topleft_coord(d, s1, s2))
