from .Layer import Layer

class WallLayer(Layer):
    def __init__(self, size, imageFile, state):
        super().__init__(size, imageFile)
        self.state = state
        self.fence_images = self.load_images([
            'assets/fence_corner_vertical.png',
            'assets/fence_corner_horizontal.png',
            'assets/fence_corner_top_left.png',
            'assets/fence_corner_top_right.png',
            'assets/fence_corner_bottom_left.png',
            'assets/fence_corner_bottom_right.png'
        ], size)

    def render(self, surface):
        for grassFlatPosition in self.state.getGrasses():
            position = self.state.getPosition(grassFlatPosition)
            position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
            surface.blit(self.image, position)
            
        for i in range(self.state.numOldRow):
            for j in range(self.state.numOldCol):
                if i != 0 and j != 0 and i + 1 != self.state.numOldRow and j + 1 != self.state.numOldCol:
                    continue
                image = self.fence_images[0]
                if i == 0 and j == 0:
                    image = self.fence_images[2]
                elif i == 0 and j + 1 == self.state.numOldCol:
                    image = self.fence_images[3]
                elif i + 1 == self.state.numOldRow and j == 0:
                    image = self.fence_images[4]
                elif i + 1 == self.state.numOldRow and j + 1 == self.state.numOldCol:
                    image = self.fence_images[5]
                elif i == 0 or i + 1 == self.state.numOldRow:
                    image = self.fence_images[1]
                position = self.state.getPosition((i, j))
                position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
                surface.blit(image, position)