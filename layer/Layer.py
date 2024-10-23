from state import GameStateObserver
import pygame

class Layer(GameStateObserver):
    def __init__(self, size, imageFile):
        self.size = size
        self.image = pygame.image.load(imageFile)
        self.image = pygame.transform.scale(self.image, size)

    def render(self, surface):
        pass