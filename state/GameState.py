from .Movable import Movable
from .Stone import Stone
from .Player import Player
from pygame.math import Vector2

class GameState:
    # '#': wall
    # ' ': free space
    # '$': stone
    # '@': Ares
    # '.': target
    # '*': stones placed on switches
    # '+': Ares on a switch
    def __init__(self, screenWidth, screenHeight, numRow, numCol, flats, stoneWeights, solutionPath):
        self.__screenHeight = screenHeight
        self.__screenWidth = screenWidth
        self.__epoch = 0
        self.__numRow = numRow
        self.__numCol = numCol
        self.__commands = [command for command in solutionPath]
        self.__flatSize = Vector2(screenWidth / numCol, screenHeight / numRow)
        self.__positions = [[Vector2(j * self.__flatSize.x + self.__flatSize.x / 2, i * self.__flatSize.y + self.__flatSize.y / 2) for j in range(numCol)] for i in range(numRow)]
        self.__observers = []
        stoneFlatPositions = self.__getStones(flats)
        playerFlatPosition = self.__getPlayer(flats)
        self.__wallFlatPositions = self.__getWalls(flats)
        self.__stones = [Stone(stoneFlatPositions[i], self.getPosition(stoneFlatPositions[i]), Vector2(1, 1), stoneWeights[i]) for i in range(len(stoneFlatPositions))]
        self.__player = Player(playerFlatPosition, self.getPosition(playerFlatPosition), Vector2(1, 1))

    def addObserver(self, observer):
        self.__observers.append(observer)
    
    def __getStones(self, flats):
        stones = []
        for i in range(self.__numRow):
            for j in range(self.__numCol):
                if flats[i][j] == '$' or flats[i][j] == '*':
                    stones.append((i, j))
        return stones
    
    def __getPlayer(self, flats):
        for i in range(self.__numRow):
            for j in range(self.__numCol):
                if flats[i][j] == '@' or flats[i][j] == '+':
                    return (i, j)
        return None
    
    def __getWalls(self, flats):
        walls = []
        for i in range(self.__numRow):
            for j in range(self.__numCol):
                if flats[i][j] == '#':
                    walls.append((i, j))
        return walls

    
    def getPosition(self, flatPosition):
        i, j = flatPosition
        return Vector2(self.__positions[i][j]) # return a copy
    
    def getStones(self):
        return self.__stones
    
    def getStone(self, position):
        for stone in self.__stones:
            if stone.getFlatPosition() == position:
                return stone
        return None
    
    def getPlayer(self):
        return self.__player
    
    def getWalls(self):
        return self.__wallFlatPositions
    
    def getFlatSize(self):
        return self.__flatSize
    
    def getNumRow(self):
        return self.__numRow
    
    def getNumCol(self):
        return self.__numCol
    
    def getCommand(self):
        if (len(self.__commands) > 0):
            return self.__commands[0]
        return None
    
    def removeCommand(self):
        if (len(self.__commands) > 0):
            print('remove')
            self.__commands.pop(0)
