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
    def __init__(self, screenWidth, screenHeight, flats, stoneWeights):
        self.__screenHeight = screenHeight
        self.__screenWidth = screenWidth
        self.normalize_grid(flats, 20, 20)
        self.__commands = None
        self.weightPath = None
        self.__flatSize = Vector2(screenWidth / self.__numCol, screenHeight / self.__numRow)
        self.__positions = [[Vector2(j * self.__flatSize.x + self.__flatSize.x / 2.0, i * self.__flatSize.y + self.__flatSize.y / 2.0) for j in range(self.__numCol)] for i in range(self.__numRow)]
        self.__observers = []
        self.__switches = self.__getSwitches(self.flats)
        stoneFlatPositions = self.__getStones(self.flats)
        playerFlatPosition = self.__getPlayer(self.flats)
        self.__grassFlatPositions = self.__getGrasses(self.flats)
        self.__wallFlatPositions = self.__getWalls(self.flats)
        self.__stones = [Stone(stoneFlatPositions[i], self.getPosition(stoneFlatPositions[i]), Vector2(1, 1), stoneWeights[i]) for i in range(len(stoneFlatPositions))]
        self.__player = Player(playerFlatPosition, self.getPosition(playerFlatPosition), Vector2(1, 1))
        self.action_log = []
        
    def set_solutionPath(self, solutionPath, weightPath):
        self.__commands = list(solutionPath)
        self.weightPath = weightPath
        self.action_log = []
    
    def normalize_grid(self, flats, target_rows, target_columns):
        self.activeNumRow = len(flats)
        self.activeNumCol = max(len(row) for row in flats)
        self.activeRow = int((target_rows - self.activeNumRow + (self.activeNumRow % 2 == 0)) / 2)
        self.activeCol = int((target_columns - self.activeNumCol + (self.activeNumCol % 2 == 0)) / 2)
        for row in flats:
            while len(row) < self.activeNumCol:
                row.append('#')
        for row in flats:
            while len(row) < target_columns:
                if len(row) % 2 == 0:
                    row.insert(0, '#')
                else:
                    row.append('#')
        while len(flats) < target_rows:
            if len(flats) % 2 == 0:
                flats.insert(0, ['#'] * target_columns)
            else:
                flats.append(['#'] * target_columns)
        self.__numCol = target_columns
        self.__numRow = target_rows
        self.flats = flats

    def addObserver(self, observer):
        self.__observers.append(observer)
    
    def __getStones(self, flats):
        stones = []
        for i in range(self.activeRow, self.activeRow + self.activeNumRow):
            for j in range(self.activeCol, self.activeCol + self.activeNumCol):
                if flats[i][j] == '$' or flats[i][j] == '*':
                    stones.append((i, j))
        return stones
    
    def __getWalls(self, flats):
        walls = []
        for i in range(self.activeRow, self.activeRow + self.activeNumRow):
            for j in range(self.activeCol, self.activeCol + self.activeNumCol):
                if flats[i][j] == '#':
                    walls.append((i, j))
        return walls
    
    def __getPlayer(self, flats):
        for i in range(self.activeRow, self.activeRow + self.activeNumRow):
            for j in range(self.activeCol, self.activeCol + self.activeNumCol):
                if flats[i][j] == '@' or flats[i][j] == '+':
                    return (i, j)
        return None
    
    def __getGrasses(self, flats):
        walls = []
        for i in range(self.activeRow + 1, self.activeRow + self.activeNumRow - 1):
            for j in range(self.activeCol + 1, self.activeCol + self.activeNumCol - 1):
                if flats[i][j] == '#':
                    walls.append((i, j))
        return walls
    
    def __getSwitches(self, flats):
        switches = []
        for i in range(self.activeRow, self.activeRow + self.activeNumRow):
            for j in range(self.activeCol, self.activeCol + self.activeNumCol):
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
            self.action_log.append(self.__commands[0])
            self.__commands.pop(0)
    
    def getScreenHeight(self):
        return self.__screenHeight
    
    def getPathCost(self):
        if len(self.action_log) == 0:
            return None
        return self.weightPath[len(self.action_log) - 1]
    
    def getStep(self):
        return len(self.action_log)
