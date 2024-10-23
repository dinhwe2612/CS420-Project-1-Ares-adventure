import pygame

class Movable:
    def __init__(self, flatPosition, position, velocity):
        self.flatPosition = flatPosition
        self.__position = position
        self.__velocity = velocity

    def move(self, vectorDirection):
        vectorDirection.normalize()
        self.__position += vectorDirection.elementwise() * self.__velocity

    def setPosition(self, position):
        self.__position = position

    def getPosition(self):
        return self.__position
    
    def setFlatPosition(self, flatPosition):
        self.flatPosition = flatPosition
    
    def getFlatPosition(self):
        return self.flatPosition
    