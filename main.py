from mode import PlayGameMode, GameModeObserver, MenuGameMode, MessageGameMode
from state import GameState
import pygame

class UserInterface(GameModeObserver):
    def __init__(self):
    
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN_WIDTH_GAME = 600
        self.SCREEN_HEIGHT_GAME = 550

        pygame.init()

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.gameState = None
        self.gameMode = MenuGameMode(self)
        self.prevGameMode = None

        self.clock = pygame.time.Clock()
        self.running = True

    def loadPlayGameMode(self, algo):
        self.gameState = GameState(self.SCREEN_WIDTH_GAME, self.SCREEN_HEIGHT_GAME, 5, 5, [
            ['#', '#', '#', '#', '#'],
            ['#', '$', '$', '$', '#'],
            ['#', '$', ' ', '$', '#'],
            ['#', '$', '$', ' ', '#'],
            ['#', '@', ' ', ' ', '#'],
        ], [1, 1, 1, 1, 1, 1, 1, 1], 'rur')
        self.gameMode = PlayGameMode(self, self.gameState)

    def showMenuRequested(self):
        self.gameMode = MenuGameMode(self)

    def showMessageBox(self, message):
        self.prevGameMode = self.gameMode
        self.gameMode = MessageGameMode(self, message)

    def backRequested(self):
        self.gameMode = self.prevGameMode
        self.prevGameMode = None

    def run(self):
        while self.running:
            self.gameMode.processInput()
            self.gameMode.update()
            self.gameMode.render(self.window)
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def applicationExit(self):
        self.running = False

userInterface = UserInterface()
userInterface.run()
