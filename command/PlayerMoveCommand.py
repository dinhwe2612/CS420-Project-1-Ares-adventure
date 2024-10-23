from .Command import Command
from pygame.math import Vector2
from .StoneMoveCommand import StoneMoveCommand

class PlayerMoveCommand(Command):
    def __init__(self, state, command):
        self.player = state.getPlayer()
        self.targetFlatPosition = self.player.getFlatPosition()
        if (command.lower() == 'r'):
            self.player.setFlip(False)
            self.direction = Vector2(1, 0)
            self.targetFlatPosition = (self.targetFlatPosition[0], self.targetFlatPosition[1] + 1)
        elif (command.lower() == 'l'):
            self.player.setFlip(True)
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
            raise Exception("Player invalid move: out of map")
        # check if the target position is a wall
        if (self.targetFlatPosition in state.getWalls()):
            raise Exception("Player invalid move: collision with wall")
        # check if the target position is a stone
        self.stoneCommand = None
        stone = state.getStone(self.targetFlatPosition)
        if (stone is not None):
            self.stoneCommand = StoneMoveCommand(state, stone, command)
        self.targetPosition = state.getPosition(self.targetFlatPosition)
        self.player.setState("walking")
        self.isDone = False

    def run(self):
        self.player.move(self.direction)
        if (self.stoneCommand != None):
            self.stoneCommand.run()
        if (abs((self.player.getPosition() - self.targetPosition).length()) < 0.1):
            self.player.setPosition(self.targetPosition)
            self.player.setState("standing")
            self.player.setFlatPosition(self.targetFlatPosition)
            self.isDone = True

    def isDone(self):
        return self.isDone