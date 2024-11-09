from .Layer import Layer
import pygame
import random

class FlatLayer(Layer):
    def __init__(self, size, state):
        self.state = state
        self.size = size
        self.flat_dirts = self.load_images([
            'assets/flat_dirt_1.png',
            'assets/flat_dirt_2.png',
            'assets/flat_dirt_3.png',
            'assets/flat_dirt_4.png',
            'assets/flat_dirt_5.png',
            'assets/flat_dirt_6.png'
        ], size)
        self.flat_grasses = self.load_images([
            'assets/flat_grass.png',
        ], size)
        self.flat_waters = self.load_images([
            'assets/water_1.png',
            'assets/water_2.png',
            'assets/water_3.png',
            'assets/water_4.png',
        ], size)
        self.flat_images_render = [] 
        num_rows = self.state.getNumRow()  
        num_cols = self.state.getNumCol()
        row_min = self.state.activeRow
        row_max = self.state.activeRow + self.state.activeNumRow - 1
        col_min = self.state.activeCol
        col_max = self.state.activeCol + self.state.activeNumCol - 1
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                if i >= row_max + 1 or j >= col_max + 1 or i < row_min or j < col_min:
                    row.append(self.get_random_flat_water())
                elif i == row_min or j == col_min or i == row_max or j == col_max:
                    row.append(self.get_random_flat_dirt())
                else:
                    row.append(self.get_random_flat_grass())
            self.flat_images_render.append(row)
        
    def load_images(self, paths, size):
        images = []
        for path in paths:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, size)
            images.append(image)
        return images
    
    def get_random_flat_dirt(self):
        return random.choice(self.flat_dirts)
    
    def get_random_flat_grass(self):
        return random.choice(self.flat_grasses)
    
    def get_random_flat_water(self):
        return random.choice(self.flat_waters)
    
    def render(self, surface):
        for i in range(self.state.getNumRow()):
            for j in range(self.state.getNumCol()):
                position = self.state.getPosition((i, j))
                position = (position.x - self.size.x / 2, position.y - self.size.y / 2)
                surface.blit(self.flat_images_render[i][j], position)
