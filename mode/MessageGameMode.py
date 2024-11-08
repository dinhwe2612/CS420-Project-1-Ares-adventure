from .GameMode import GameMode
import pygame

class MessageGameMode(GameMode):
    def __init__(self, observer, message, screenHeight, screenWidth):
        super().__init__(observer, screenHeight, screenWidth)

    def render(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((222, 0, 0, 0))  # Black color with 50% transparency
        surface.blit(overlay, (0, 0))
        super().render(surface)