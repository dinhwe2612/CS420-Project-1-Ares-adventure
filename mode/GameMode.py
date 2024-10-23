import pygame

class GameMode():
    def __init__(self, observer):
        self.observer = observer
        self.buttons = []
        self.textviews = []

    def addButton(self, button):
        self.buttons.append(button)

    def addTextView(self, textview):
        self.textviews.append(textview)

    def notifyGameFinished(self):
        self.observer.gameFinished()
    
    def notifyGameFailed(self, message):
        self.observer.gameFailed(message)

    def notifyShowMenuRequested(self):
        self.observer.showMenuRequested()

    def notifyLoadPlayGameMode(self, algo):
        self.observer.loadPlayGameMode(algo)
    
    def notifyShowMessageBox(self, message):
        self.observer.showMessageBox(message)

    def notifyBackRequested(self):
        self.observer.backRequested()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.observer.applicationExit()
            for button in self.buttons:
                button.get_event(event)
        
    
    def update(self):
        for button in self.buttons:
            button.update()
    
    def render(self, surface):
        for button in self.buttons:
            button.render(surface)
        for textview in self.textviews:
            textview.render(surface)