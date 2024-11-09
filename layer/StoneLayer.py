from .Layer import Layer
import pygame

class StoneLayer(Layer):
    def __init__(self, size, imageFile, state):
        super().__init__(size, imageFile)
        self.state = state
        self.font = pygame.font.Font(None, int(size[0] * 0.7))

    def render(self, surface):
        for stone in self.state.getStones():
            position = stone.getPosition()
            position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
            surface.blit(self.image, position)
            text_surface = self.font.render(str(stone.getWeight()), True, (128,0,0))
            surface.blit(text_surface, text_surface.get_rect(center=stone.getPosition()))
            