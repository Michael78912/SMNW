"""handles the music for this game."""

import pygame
import os
from database import Area



def play(game_state):
    pygame.mixer.music.load(
        os.path.join('music',
            {
                Area.MAP: 'smnwtheme.mp3',
                Area.TITLE: 'smnwtheme.mp3'
                Area.STAGE: 'smnwgameplay.mp3',
                Area.BOSS:'smnwboss.mp3'
            }[game_state['AREA']]
        )
    )
    pygame.mixer.music.play(-1)

def check(settings):
    """check the settings to see if we should turn the music off."""
