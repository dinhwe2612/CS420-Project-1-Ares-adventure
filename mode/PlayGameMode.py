from mode import GameMode
from state import GameState
from layer import FlatLayer, StoneLayer, PlayerLayer, WallLayer, SwitchLayer
from command import PlayerMoveCommands, PlayerMoveCommand
from pygame.math import Vector2
from pygame_gui.elements import UIButton, UIDropDownMenu, UITextBox
import pygame
import pygame_gui

class PlayGameMode(GameMode):
    def __init__(self, observer, gameState, screenHeight, screenWidth):
        super().__init__(observer, screenHeight, screenWidth)
        
        self.gameState = gameState
        self.layers = [
            FlatLayer(gameState.getFlatSize(), self.gameState),
            SwitchLayer(gameState.getFlatSize(), 'assets/switch_1.png', self.gameState),
            WallLayer(gameState.getFlatSize(), 'assets/wall.png', self.gameState),
            StoneLayer(gameState.getFlatSize(), 'assets/stone.png', self.gameState),
            PlayerLayer(gameState.getFlatSize(), 'assets/player.json', self.gameState)
        ]

        for layer in self.layers:
            self.gameState.addObserver(layer)
        
        self.back_button = UIButton(relative_rect=pygame.Rect(630, 140, 140, 40),
                                    text='Back',
                                    manager=self.ui_manager)
        
        self.run_button = UIButton(relative_rect=pygame.Rect(630, 90, 140, 40),
                                   text = 'Run',
                                   manager=self.ui_manager)
        self.steps_text = """<p>Steps: <p><p>Node: <p><p>Time (ms): <p><p>Memory (MB): <p><p>Path Solution: <p>"""
        self.steps_textbox = UITextBox(
            relative_rect=pygame.Rect((610, 195), (180, 400)),  # Position and size
            html_text=self.steps_text,
            manager=self.ui_manager
        )
        
        self.algo = 'A*'
        dropdown_algo_options = ['DFS', 'BFS', 'UCS', 'A*']
        self.dropdown_algo = UIDropDownMenu(
            options_list=dropdown_algo_options,
            starting_option=dropdown_algo_options[3],
            relative_rect=pygame.Rect(630, 10, 140, 30),  # Position and size of the dropdown
            manager=self.ui_manager
        )
        
        dropdown_map_options = []
        for i in range(10):
            dropdown_map_options.append(f'input-{str(i + 1).zfill(2)}.txt')
        self.dropdown_map = UIDropDownMenu(
            options_list=dropdown_map_options,
            starting_option=dropdown_map_options[0],
            relative_rect=pygame.Rect(630, 50, 140, 30),  # Position and size of the dropdown
            manager=self.ui_manager
        )

        self.commands = []
        try:
            self.commands.append(PlayerMoveCommands(self.gameState))
        except Exception as e:
            messageError = str(e)
            self.notifyShowMessageBox(messageError)
            print(messageError)
            
    def processInput(self, event):
        super().processInput(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.run_button:
                print('run')
            if event.ui_element == self.back_button:
                self.observer.showMenuRequested()
                
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.dropdown_algo:
                self.algo = event.text
            
            if event.ui_element == self.dropdown_map:
                print(event.text)

    def update(self, delta_time):
        super().update(delta_time)
        for command in self.commands:
            try:
                command.run()
                if command.isDone():
                    self.commands.remove(command)
            except Exception as e:
                messageError = str(e)
                self.notifyShowMessageBox(messageError)

    def render(self, surface):
        surface.fill((229, 228, 226))
        for layer in self.layers:
            layer.render(surface)
        super().render(surface)