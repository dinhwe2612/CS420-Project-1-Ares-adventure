from .Movable import Movable

class Stone(Movable):
    def __init__(self, flatPosition, position, velocity, weight):
        super().__init__(flatPosition, position, velocity)
        self.__weight = weight

    def getWeight(self):
        return self.__weight