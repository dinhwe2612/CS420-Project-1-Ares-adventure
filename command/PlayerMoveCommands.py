from .Command import Command
from .PlayerMoveCommand import PlayerMoveCommand

class PlayerMoveCommands(Command):
    def __init__(self, state):
        if (state.getCommand() == None):
            raise Exception("PlayerMoveCommands: empty commands")
        self.state = state
        print(state.getCommand())
        self.currentCommand = PlayerMoveCommand(state, state.getCommand())
        self.state.removeCommand()

    def run(self):
        self.currentCommand.run()
        if (self.currentCommand.isDone):
            
            command = self.state.getCommand()
            print(command)
            if (command != None):
                self.currentCommand = PlayerMoveCommand(self.state, command)
                self.state.removeCommand()
    
    def isDone(self):
        return self.state.getCommand() == None