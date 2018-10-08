"""
this class is the base class
for all things like enemies, and characters.
"""

import pygame as pg
import threading


class IDontKnowWhatToCallItYet:
    def start_thread(self, **kwargs):
        self.mainthread = threading.Thread(
            target=self.mainloop, daemon=True, **kwargs)
        self.mainthread.start()

    def mainloop(self):
        pass
        # this needs to be figured out yet.
        # i figure i can do that when i get more
        # of the workings figured out

    def kill_thread(self):
        self.
