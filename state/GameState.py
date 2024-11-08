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
        self.__numRow = numRow
        self.__numCol = numCol
        self.numOldRow = numRow
        self.numOldCol = numCol
        self.normalize_grid(flats, 15, 15)
        self.__commands = [command for command in solutionPath]
        self.__flatSize = Vector2(screenWidth / self.__numCol, screenHeight / self.__numRow)
        self.__positions = [[Vector2(j * self.__flatSize.x + self.__flatSize.x / 2.0, i * self.__flatSize.y + self.__flatSize.y / 2.0) for j in range(self.__numCol)] for i in range(self.__numRow)]
        self.__observers = []
        self.__switches = self.__getSwitches(flats)
        stoneFlatPositions = self.__getStones(flats)
        playerFlatPosition = self.__getPlayer(flats)
        self.__grassFlatPositions = self.__getGrasses(flats)
        self.__wallFlatPositions = self.__getWalls(flats)
        self.__stones = [Stone(stoneFlatPositions[i], self.getPosition(stoneFlatPositions[i]), Vector2(1, 1), stoneWeights[i]) for i in range(len(stoneFlatPositions))]
        self.__player = Player(playerFlatPosition, self.getPosition(playerFlatPosition), Vector2(1, 1))
    
    def normalize_grid(self, flats, target_rows, target_columns):
        # Ensure each row has exactly target_columns elements by adding '#' if needed
        for row in flats:
            if self.__numCol < target_columns:
                row.extend(['#'] * (target_columns - self.__numCol))
        # If there are fewer than target_rows, add new rows filled with '#' to reach the target
        while self.__numRow < target_rows:
            flats.append(['#'] * target_columns)
            self.__numRow += 1
        self.__numCol = target_columns

    def addObserver(self, observer):
        self.__observers.append(observer)
    
    def __getStones(self, flats):
        stones = []
        for i in range(self.__numRow):
            for j in range(self.__numCol):
                if flats[i][j] == '$' or flats[i][j] == '*':
                    stones.append((i, j))
        return stones
    
    def __getWalls(self, flats):
        walls = []
        for i in range(self.numOldRow):
            for j in range(self.numOldCol):
                if flats[i][j] == '#':
                    walls.append((i, j))
        return walls
    
    def __getPlayer(self, flats):
        for i in range(self.__numRow):
            for j in range(self.__numCol):
                if flats[i][j] == '@' or flats[i][j] == '+':
                    return (i, j)
        return None
    
    def __getGrasses(self, flats):
        walls = []
        for i in range(self.numOldRow):
            if i == 0 or i + 1 == self.numOldRow:
                continue
            for j in range(self.numOldCol):
                if j == 0 or j + 1 == self.numOldCol:
                    continue
                if flats[i][j] == '#':
                    walls.append((i, j))
        return walls
    
    def __getSwitches(self, flats):
        switches = []
        for i in range(self.numOldRow):
            for j in range(self.numOldCol):
                if flats[i][j] == '+' or flats[i][j] == '*' or flats[i][j] == '.':
                    switches.append((i, j))
        return switches
    
    def getWalls(self):
        return self.__wallFlatPositions
    
    def getPosition(self, flatPosition):
        i, j = flatPosition
        return Vector2(self.__positions[i][j])
    
    def getSwitches(self):
        return self.__switches
    
    def getStones(self):
        return self.__stones
    
    def getStone(self, position):
        for stone in self.__stones:
            if stone.getFlatPosition() == position:
                return stone
        return None
    
    def getPlayer(self):
        return self.__player
    
    def getGrasses(self):
        return self.__grassFlatPositions
    
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
    
    def getScreenHeight(self):
        return self.__screenHeight
