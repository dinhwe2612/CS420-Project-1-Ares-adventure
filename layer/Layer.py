from state import GameStateObserver
import pygame

class Layer(GameStateObserver):
    def __init__(self, size, imageFile):
        self.size = size
        self.image = pygame.image.load(imageFile)
        self.image = pygame.transform.scale(self.image, size)
        
    def load_images(self, paths, size):
        images = []
        for path in paths:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, size)
            images.append(image)
        return images

    def render(self, surface):
        pass