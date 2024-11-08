import pygame
import pygame_gui

class GameMode():
    def __init__(self, observer, screenHeight, screenWidth):
        self.observer = observer
        self.ui_manager = pygame_gui.UIManager((screenWidth, screenHeight), 'assets/theme.json')

    def notifyGameFinished(self):
        self.observer.gameFinished()
    
    def notifyGameFailed(self, message):
        self.observer.gameFailed(message)

    def notifyShowMenuRequested(self):
        self.observer.showMenuRequested()

    def notifyLoadPlayGameMode(self):
        self.observer.loadPlayGameMode()
    
    def notifyShowMessageBox(self, message):
        self.observer.showMessageBox(message)

    def notifyBackRequested(self):
        self.observer.backRequested()

    def processInput(self, event):
        if event.type == pygame.QUIT:
            self.observer.applicationExit()
        self.ui_manager.process_events(event)
    
    def update(self, delta_time):
        self.ui_manager.update(delta_time)
    
    def render(self, surface):
        self.ui_manager.draw_ui(surface)