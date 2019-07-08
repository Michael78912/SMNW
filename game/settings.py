"""settings.py- displays and changes the settings
for stickman's new world.
if the user settings
"""

import os

import pygame
import music

import database

pygame.init()

def get_switches(game_state):
    """get a bunch of Switch objects each representing the thing."""
    settings = game_state['SETTINGS']

    switches = []

    y = 200

    for setting, value in zip(settings, settings.values()):
        switches.append(Switch((400, y), value, setting))
        y += 100

    return switches


class Switch:
    """class for displaying a switch.
    will show as on if true, as off if false.
    """

    rect = None

    def __init__(self, pos, state, text):
        self.pos = pos
        self.state = state
        self.text = text

    def draw(self, surf):
        """draw the switch to surf."""
        font = pygame.font.Font(os.path.join('data', 'Michael`s Font.ttf'), 22)
        text: pygame.Surface = font.render(self.text, True, (255, 255, 255))
        width = text.get_width() + 70
        switchsurf = pygame.Surface((width, 24))
        switchsurf.blit(text, (0, 0))
        switchsurf.blit(self._surface, (text.get_width() + 10, 0))
        rect: pygame.Rect = switchsurf.get_rect()
        rect.center = self.pos
        self.rect = rect
        surf.blit(switchsurf, rect)

    @property
    def _surface(self):
        surf = pygame.Surface((60, 24))
        surf.fill((0, 0, 255))
        square_rect = pygame.Rect(
            4 if not self.state else 40,
            4,
            16,
            16,
        )
        surf.blit(pygame.Surface((16, 16)), square_rect)
        return surf


def main(game_state, bgimage):
    """run the main settings function."""
    
    # font file
    fontfile = os.path.join('data', 'Michael`s Font.ttf')
    # font objects
    font_header = pygame.font.Font(fontfile, 70)
    font_button = pygame.font.Font(fontfile, 30)

    # extract the two needed things for this function
    settings = game_state['SETTINGS']
    surf = game_state['MAIN_DISPLAY_SURF']

    # generate the list of switches needed for each setting
    switches = get_switches(game_state)

    # button to return to the main screen.
    return_btn: pygame.Surface = font_button.render('Return', True, (255, 255, 255))

    # rectangle object bound to return button
    return_rect = return_btn.get_rect(center=(400, 560))

    # header to be drawn and show the user where they are.
    header = font_header.render('Settings', True, (255, 255, 255))

    # used to determine where the header should go.
    header_rect = header.get_rect(center=(400, 70))

    while True:
        # check the settings to handle the music.
        music.check(game_state)
        
        # background image to be drawn first
        surf.blit(bgimage, (0, 0))

        # draw the return button
        surf.blit(return_btn, return_rect)

        # draw the settings header
        surf.blit(header, header_rect)

        # draw each switch
        for switch in switches:
            switch.draw(surf)

        # event handler
        for event in pygame.event.get():
            # check for quits
            if event.type == pygame.QUIT:
                raise SystemExit

            # check to see if anything was clicked on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check to see if the return button was clicked.
                if return_rect.collidepoint(event.pos):
                    # return to previous screen
                    return

                # check all switches
                for switch in switches:
                    # someone clicked on a switch
                    if switch.rect.collidepoint(event.pos):
                        # switch the state (False -> True, True -> False)
                        switch.state = not switch.state
                        # update the setting
                        settings[switch.text] = switch.state
                        print(settings)
        # add the cursor (always in the foreground)
        surf.blit(database.PICS['cursor'], pygame.mouse.get_pos())
        # update screen
        pygame.display.update()

    # Switch(None, False, "Hello").draw(pygame.Surface((1, 1)))
