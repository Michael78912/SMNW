"""handles the music for this game."""

import pygame
import os
from database import Area



def play(game_state):
    pygame.mixer.music.load(
        os.path.join('music',
            {
                1: 'smnwtheme.mp3',
                0: 'smnwtheme.mp3',
                3: 'smnwgameplay.mp3',
                2: 'smnwgameplay.mp3',
                4:'smnwboss.mp3',
            }[game_state['AREA']]
        )
    )
    pygame.mixer.music.play(-1)

def check(game_state):
    """check the settings to see if we should turn the music off."""
    settings = game_state['SETTINGS']
    if settings['music'] and pygame.mixer.music.get_busy():
        # already playing music and music is enabled.
        pass
    
    if settings['music'] and not pygame.mixer.music.get_busy():
        # not playing, but should be. start playing
        play(game_state)
    
    if not settings['music'] and pygame.mixer.music.get_busy():
        # playing music, but shouldn't be. stop
        pygame.mixer.music.fadeout(400)
