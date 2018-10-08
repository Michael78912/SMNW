from class_.events import *


def put_all(main_game_state, event):
    for sprite in main_game_state.sprites():
        sprite.internal_event(event)


def quit_all(main_game_state):
    put_all(main_game_state, Quit())
