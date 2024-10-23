from .GameMode import GameMode
from ui import TextView, Button
import pygame

TITLE_MESSAGE_SETTINGS = {
    'bg': (0, 0, 0),
    'fg': (255, 255, 255),
    'font': 'BD_Cartoon_Shout',
    'fontsize': 8
}
BUTTON_SETTINGS = {
    'hover'   : (155,155,155),
    'font'    : 'BD_Cartoon_Shout',
    'fg'      : (0,0,0),
    'bg'      : (255,255,255),
    'border'  : False,
    'fontsize': 25
}

class MessageGameMode(GameMode):
    def __init__(self, observer, message):     
        super().__init__(observer)
        title_tv = TextView(position=(350, 150), text=message, width=300, height=200, **TITLE_MESSAGE_SETTINGS)
        self.addTextView(title_tv)
        self.addButton(
            Button(position=(700, 100), text='Back', width=100, height=50, command=lambda: self.notifyBackRequested(), **BUTTON_SETTINGS)
        )

    def render(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((222, 0, 0, 0))  # Black color with 50% transparency
        surface.blit(overlay, (0, 0))
        super().render(surface)