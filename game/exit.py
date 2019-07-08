"""exit.py- this has two functions, exit and special_exit.
special_exit will be called only in the event of an exeption.
"""

import json
import traceback
import os
import time

from database import SAVE_DIR

LOGTEXT = """
---> Oops, it appears I did something stupid. ({})

{}

"""

class _StreamAbsorber:
    contents = ''
    def write(self, text):
        """add text to contents"""
        self.contents += text

    @staticmethod
    def flush():
        """do absolutely nothing"""
        pass


def exit(game_state):
    """exit the game and save things like settings."""
    with open(os.path.join(SAVE_DIR, 'settings.json'), 'w') as file:
        file.write(json.dumps(game_state['SETTINGS']))


def special_exit(game_state):
    """exit the game, but leave a crash log."""
    exit(game_state)

    fake_file = _StreamAbsorber()

    with open(os.path.join(SAVE_DIR, 'CRASH.LOG'), 'a') as file:
        traceback.print_exc(file=fake_file)
        file.write(LOGTEXT.format(time.asctime(), fake_file.contents))

