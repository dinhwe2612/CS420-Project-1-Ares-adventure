from .Movable import Movable

class Player(Movable):
    def __init__(self, flatPosition, position, velocity):
        super().__init__(flatPosition, position, velocity)
        self.__state = "standing"
        self.__isFlip = False
        
    def getState(self):
        return self.__state
    
    def setState(self, state):
        self.__state = state

    def setFlip(self, isFlip):
        self.__isFlip = isFlip

    def isFlip(self):
        return self.__isFlip

    def isWalking(self):
        return self.__state == "walking"
    
    def isPushing(self):
        return self.__state == "pushing"