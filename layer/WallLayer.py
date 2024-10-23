from .Layer import Layer

class WallLayer(Layer):
    def __init__(self, size, imageFile, state):
        super().__init__(size, imageFile)
        self.state = state

    def render(self, surface):
        for wallFlatPosition in self.state.getWalls():
            position = self.state.getPosition(wallFlatPosition)
            position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
            surface.blit(self.image, position)