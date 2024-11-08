from .Layer import Layer

class SwitchLayer(Layer):
    def __init__(self, size, imageFile, state):
        super().__init__(size, imageFile)
        self.state = state

    def render(self, surface):
        for switch in self.state.getSwitches():
            position = self.state.getPosition(switch)
            position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
            surface.blit(self.image, position)