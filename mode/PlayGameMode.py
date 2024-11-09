from mode import GameMode
from state import GameState
from layer import FlatLayer, StoneLayer, PlayerLayer, WallLayer, SwitchLayer
from command import PlayerMoveCommands, PlayerMoveCommand
from pygame.math import Vector2
from pygame_gui.elements import UIButton, UIDropDownMenu, UITextBox
import pygame
import pygame_gui
from algo import read_level

class PlayGameMode(GameMode):
    def __init__(self, observer, screenHeight, screenWidth, screenHeightGame, screenWidthGame):
        super().__init__(observer, screenHeight, screenWidth)
        
        self.map = None
        
        self.screenHeightGame = screenHeightGame
        self.screenWidthGame = screenWidthGame
        
        self.load_map("input-01.txt")
        
        self.back_button = UIButton(relative_rect=pygame.Rect(630, 140, 140, 40),
                                    text='Back',
                                    manager=self.ui_manager)
        
        self.run_button = UIButton(relative_rect=pygame.Rect(630, 90, 140, 40),
                                   text = 'Run',
                                   manager=self.ui_manager)
        self.steps_text = """<p>Node: </p><p>Time (ms): </p><p>Memory (MB): </p><p>Steps: {num_steps}</p><p>Path Cost: {path_cost}</p><p>Path Solution: </p><p>{action_log}</p>"""
        updated_text = self.steps_text.format(num_steps='', path_cost='', action_log='')
        self.steps_textbox = UITextBox(
            relative_rect=pygame.Rect((610, 195), (180, 400)),  # Position and size
            html_text=updated_text,
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
        
        self.loading_popup = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((250, 200), (300, 150)),
            manager=self.ui_manager,
            window_display_title="Loading",
            object_id="#loading_popup"
        )
        
        self.loading_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 50), (200, 30)),
            text="Loading, please wait...",
            manager=self.ui_manager,
            container=self.loading_popup
        )
        self.loading_popup.hide()

    def run_solutionPath(self, solutionPath, weightPath):
        self.loading_popup.hide()
        self.run_button.set_text('Pause')
        self.solution_path = solutionPath
        self.weight_path = weightPath
        self.start = True
        self.gameState.set_solutionPath(solutionPath, weightPath)
        try:
            self.commands.append(PlayerMoveCommands(self.gameState))
        except Exception as e:
            messageError = str(e)
            self.notifyShowMessageBox(messageError)
            print(messageError)
    
    def load_map(self, mapPath):
        self.grid, self.stone_weights = read_level("input/" + mapPath)
        for i in self.grid:
            print(i)
        print(self.stone_weights)
        self.gameState = GameState(self.screenHeightGame, self.screenWidthGame, self.grid, self.stone_weights)
        if self.map != mapPath:
            self.solution_path = None
            self.map = mapPath
        self.start = False
        self.commands = []
        self.layers = [
            FlatLayer(self.gameState.getFlatSize(), self.gameState),
            SwitchLayer(self.gameState.getFlatSize(), 'assets/switch_1.png', self.gameState),
            WallLayer(self.gameState.getFlatSize(), 'assets/wall.png', self.gameState),
            StoneLayer(self.gameState.getFlatSize(), 'assets/stone.png', self.gameState),
            PlayerLayer(self.gameState.getFlatSize(), 'assets/player.json', self.gameState)
        ]
        for layer in self.layers:
            self.gameState.addObserver(layer)

    def start_pressed(self):
        if self.solution_path == None:
            self.loading_popup.show()
            self.observer.run_algorithm(self.grid, self.stone_weights, self.algo)
        elif len(self.commands) > 0:
            self.start = not self.start
            if self.start:
                self.run_button.set_text('Pause')
            else:
                self.run_button.set_text('Continue')
        else:
            self.load_map(self.map)
            self.run_solutionPath(self.solution_path, self.weight_path)
            self.start = True

    def processInput(self, event):
        super().processInput(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.run_button:
                self.start_pressed()
            if event.ui_element == self.back_button:
                self.observer.showMenuRequested()
                
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.dropdown_algo:
                self.algo = event.text
            
            if event.ui_element == self.dropdown_map:
                self.load_map(event.text)
                
    def update_textbox(self):
        num_steps = self.gameState.getStep() if self.gameState.getStep() is not None else ""
        path_cost = self.gameState.getPathCost() if self.gameState.getPathCost() is not None else ""
        action_log = self.gameState.action_log if self.gameState.action_log is not None else ""
        updated_text = self.steps_text.format(num_steps=num_steps, path_cost=path_cost, action_log=action_log)
        self.steps_textbox.set_text(updated_text)

    def update(self, delta_time):
        super().update(delta_time)
        if self.start:
            self.update_textbox()
            if self.commands == None:
                self.start = None
                self.run_button.set_text('Start')
            elif len(self.commands) == 0 and len(self.solution_path) > 0:
                self.start = None
                self.run_button.set_text('Restart')
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