from .GameMode import GameMode
import pygame
import pygame_gui
from pygame_gui.elements import UIButton

class MenuGameMode(GameMode):
    def __init__(self, observer, screenHeight, screenWidth):
        super().__init__(observer, screenHeight, screenWidth)
        
        self.start_button = UIButton(relative_rect=pygame.Rect(0, 140, 160, 100),
                                    text='Start', manager=self.ui_manager,
                                    anchors={'centerx': 'centerx'})
        self.exit_button = UIButton(relative_rect=pygame.Rect(0, 90, 160, 100),
                                    text='Exit', manager=self.ui_manager,
                                    anchors={
                                        'centerx': 'centerx',
                                        'top_target': self.start_button
                                        })
        
    def processInput(self, event):
        super().processInput(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element ==  self.start_button:
                self.notifyLoadPlayGameMode()
            if event.ui_element == self.exit_button:
                self.observer.applicationExit()
    def update(self, delta_time):
        super().update(delta_time)
    
    def render(self, surface):
        surface.fill((0, 0, 0))
        super().render(surface)
        