from mode import PlayGameMode, GameModeObserver, MenuGameMode, MessageGameMode
from state import GameState
import pygame
import pygame_gui

class UserInterface(GameModeObserver):
    def __init__(self):
    
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN_WIDTH_GAME = 600
        self.SCREEN_HEIGHT_GAME = 600

        pygame.init()

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.gameState = None
        self.gameMode = MenuGameMode(self, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
        self.prevGameMode = None

        self.clock = pygame.time.Clock()
        self.running = True

    def loadPlayGameMode(self):
        self.gameState = GameState(self.SCREEN_WIDTH_GAME, self.SCREEN_HEIGHT_GAME, 7, 10, [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', '.', ' ', '.', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', '@', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '$', ' ', ' ', '.', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ], [2, 3, 1], 'llldRRRuullluRRurDRurD')
        self.gameMode = PlayGameMode(self, self.gameState, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)

    def showMenuRequested(self):
        self.gameMode = MenuGameMode(self, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)

    def showMessageBox(self, message):
        self.prevGameMode = self.gameMode
        self.gameMode = MessageGameMode(self, message, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)

    def backRequested(self):
        self.gameMode = self.prevGameMode
        self.prevGameMode = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.gameMode.processInput(event)
            time_delta = self.clock.tick(60) / 1000.0
            self.gameMode.update(time_delta)
            self.gameMode.render(self.window)
            pygame.display.update()
            
        pygame.quit()

    def applicationExit(self):
        self.running = False

userInterface = UserInterface()
userInterface.run()
