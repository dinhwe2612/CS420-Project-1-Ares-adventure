from .Command import Command
from pygame.math import Vector2

class StoneMoveCommand(Command):
    def __init__(self, state, stone, command):
        self.stone = stone
        self.targetFlatPosition = self.stone.getFlatPosition()
        if (command.lower() == 'r'):
            self.direction = Vector2(1, 0)
            self.targetFlatPosition = (self.targetFlatPosition[0], self.targetFlatPosition[1] + 1)
        elif (command.lower() == 'l'):
            self.direction = Vector2(-1, 0)
            self.targetFlatPosition = (self.targetFlatPosition[0], self.targetFlatPosition[1] - 1)
        elif (command.lower() == 'u'):
            self.direction = Vector2(0, -1)
            self.targetFlatPosition = (self.targetFlatPosition[0] - 1, self.targetFlatPosition[1])
        else:
            self.direction = Vector2(0, 1)
            self.targetFlatPosition = (self.targetFlatPosition[0] + 1, self.targetFlatPosition[1])
        # check if the target position is out of map
        if (self.targetFlatPosition[0] < 0 or self.targetFlatPosition[0] >= state.getNumRow() or self.targetFlatPosition[1] < 0 or self.targetFlatPosition[1] >= state.getNumCol()):
            raise Exception("Stone invalid move: out of map")
        # check if the target position is a wall
        if (self.targetFlatPosition in state.getWalls()):
            raise Exception("Stone invalid move: collision with wall")
        # check if the target position is a stone
        if (state.getStone(self.targetFlatPosition) is not None):
            raise Exception("Stone invalid move: collision with stone")
        self.targetPosition = state.getPosition(self.targetFlatPosition)
        self.isDone = False

    def run(self):
        self.stone.move(self.direction)
        if (abs((self.stone.getPosition() - self.targetPosition).length()) < 0.1):
            self.stone.setPosition(self.targetPosition)
            self.stone.setFlatPosition(self.targetFlatPosition)
            self.isDone = True

    def isDone(self):
        return self.isDone