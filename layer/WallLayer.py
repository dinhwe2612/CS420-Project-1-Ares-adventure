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
        row_min = self.state.activeRow
        row_max = self.state.activeRow + self.state.activeNumRow - 1
        col_min = self.state.activeCol
        col_max = self.state.activeCol + self.state.activeNumCol - 1
        for i in range(row_min, row_max + 1):
            for j in range(col_min, col_max + 1):
                if i != row_min and j != col_min and i != row_max and j != col_max:
                    continue
                image = self.fence_images[0]
                if i == row_min and j == col_min:
                    image = self.fence_images[2]
                elif i == row_min and j == col_max:
                    image = self.fence_images[3]
                elif i == row_max and j == col_min:
                    image = self.fence_images[4]
                elif i == row_max and j == col_max:
                    image = self.fence_images[5]
                elif i == row_min or i == row_max:
                    image = self.fence_images[1]
                position = self.state.getPosition((i, j))
                position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
                surface.blit(image, position)