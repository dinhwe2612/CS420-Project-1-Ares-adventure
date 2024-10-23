from .Layer import Layer
import pygame

class FlatLayer(Layer):
    def __init__(self, size, imageFile, state):
        super().__init__(size, imageFile)
        self.state = state

    def render(self, surface):
        for i in range(self.state.getNumRow()):
            for j in range(self.state.getNumCol()):
                position = self.state.getPosition((i, j))
                position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
                surface.blit(self.image, position)
