"""runs the debug terminal for SMWN."""
import collections
import threading
import logging
import copy

import gameterm
import pygame

from database import MAIN_GAME_STATE
import database
import class_


def handle(event):
    """check to see if the event is proper. if it is, then start
    the terminal.
    """
    if event.type == pygame.KEYDOWN and event.unicode == '~':
        # now we can open the terminal
        start_terminal()

    if MAIN_GAME_STATE.get('TERMINAL'):
        MAIN_GAME_STATE['TERMINAL'].add_event(event)


def start_terminal(pos=(150, 0)):
    """start the game terminal"""
    game_state = MAIN_GAME_STATE
    prev = game_state.get('TERMINAL')

    if prev is not None:
        logging.info('removing previous terminal')
        game_state['TERMINAL'].kill()
        del game_state['TERMINAL']
    
    logging.info('initializing shell')

    shell = gameterm.shell.Shell(
        gameterm.terminal.Terminal(
            game_state['MAIN_DISPLAY_SURF'],
            # half transparent background
            bgcolour=(0, 0, 200, 150),
            fgcolour=(200, 0, 0),
        ),
        game_state['MAIN_DISPLAY_SURF'],
        pos,
        prompt="SMNW debug shell> "
    )
    shell.bind()
    # remove the ~ sent to the terminal.
    fake_event = collections.namedtuple('fake_event', ['type', 'unicode'])
    ev = fake_event(pygame.KEYDOWN, '\b')
    shell.terminal.input(ev)

    @shell.command
    def to_map(
        char1: "first character",
        char2: "second character",
        char3: "third character",
        char4: "fourth character",
    ):
        """send to map with default weapons, and the characters, in order."""
        namestotypes = {
            'swordsman': class_.Swordsman,
            'angel': class_.Angel,
            'archer': class_.Archer,
            'spearman': class_.Spearman,
            'wizard': class_.Wizard,
        }
        logging.info("moving to map with characters {}, {}, {}, {}".format(
            char1, char2, char3, char4,
        ))
        try:
            game_state['PLAYERS'] = [
                namestotypes[char1](1, game_state, copy.copy(
                    database.DEFAULT_WEAPONS[char1]
                )),
                namestotypes[char2](2, game_state, copy.copy(
                    database.DEFAULT_WEAPONS[char2]
                )),
                namestotypes[char3](3, game_state, copy.copy(
                    database.DEFAULT_WEAPONS[char3]
                )),
                namestotypes[char4](4, game_state, copy.copy(
                    database.DEFAULT_WEAPONS[char4]
                )),
            ]

        except KeyError:
            print('Error: unrecognised character')

        game_state['AREA'] = database.Area.MAP

    @shell.command
    def exit():
        """stop the terminal thread."""
        game_state['TERMINAL'] = None
        shell.kill()

    @shell.command
    def reset():
        """reset the state of the terminal."""
        shell.terminal.reset()
    
    @shell.command
    def execute(code):
        """execute the code as python code. USE WITH CAUTION!

        May cause brain damage, and other deadly symptoms if used incorrectly.
        """
        logging.info('executing "{}"'.format(code))
        exec(code)

    threading.Thread(target=shell.mainloop, args=(60,), daemon=True).start()
    game_state['TERMINAL'] = shell
