import pygame
import os
class Font:
    '''simulating tools'''
    path = 'assets/fonts'
    @staticmethod
    def load(filename, size):
        p = os.path.join(Font.path, filename+'.ttf')
        return pygame.font.Font(os.path.abspath(p), size)