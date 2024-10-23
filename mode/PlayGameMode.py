from mode import GameMode
from state import GameState
from layer import FlatLayer, StoneLayer, PlayerLayer, WallLayer
from command import PlayerMoveCommands, PlayerMoveCommand
from pygame.math import Vector2
from ui import Button, TextView

COMMAND_TEXT_SETTINGS = {
    'bg': (0, 0, 0),
    'fg': (255, 255, 255),
    'font': 'BD_Cartoon_Shout',
    'fontsize': 15
}
BUTTON_SETTINGS = {
            'hover'   : (155,155,155),
            'font'    : 'BD_Cartoon_Shout',
            'fg'      : (255,255,255),
            'bg'      : (0,0,0),
            'border'  : False,
            'fontsize': 25
        }

class PlayGameMode(GameMode):
    def __init__(self, observer, gameState):
        super().__init__(observer)

        self.gameState = gameState
        self.layers = [
            FlatLayer(gameState.getFlatSize(), 'assets/flat.png', self.gameState),
            WallLayer(gameState.getFlatSize(), 'assets/wall.png', self.gameState),
            StoneLayer(gameState.getFlatSize(), 'assets/stone.png', self.gameState),
            PlayerLayer(gameState.getFlatSize(), 'assets/player.json', self.gameState)
        ]

        for layer in self.layers:
            self.gameState.addObserver(layer)

        self.addButton(
            Button(position=(700, 100), text='Back', width=100, height=50, command=lambda: self.notifyShowMenuRequested(), **BUTTON_SETTINGS)
        )

        self.addTextView(
            TextView(position=(10, 570), text='Play Game', width=600, height=100, **COMMAND_TEXT_SETTINGS)
        )

        self.commands = []
        try:
            self.commands.append(PlayerMoveCommands(self.gameState))
        except Exception as e:
            messageError = str(e)
            self.notifyShowMessageBox(messageError)

    def update(self):
        super().update()
        for command in self.commands:
            try:
                command.run()
                if command.isDone():
                    self.commands.remove(command)
            except Exception as e:
                messageError = str(e)
                self.notifyShowMessageBox(messageError)

    def render(self, surface):
        surface.fill((0, 0, 0))
        for layer in self.layers:
            layer.render(surface)
        super().render(surface)