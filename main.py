from mode import PlayGameMode, GameModeObserver, MenuGameMode, MessageGameMode
from state import GameState
from algo import read_level
from algo import turnIntoTuple
from algo import SokobanProblem
from algo import breadth_first_search
from algo import depth_first_search
from algo import uniform_cost_search
from algo import best_first_search
from algo import f
from algo import process_result
import pygame
import pygame_gui
import threading

class UserInterface(GameModeObserver):
    def __init__(self):
    
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN_WIDTH_GAME = 600
        self.SCREEN_HEIGHT_GAME = 550

        pygame.init()

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.ui_manager = pygame_gui.UIManager((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.gameState = None
        self.gameMode = MenuGameMode(self)
        self.prevGameMode = None

        self.clock = pygame.time.Clock()
        self.running = True

    def loadPlayGameMode(self, level, algo):
        # Define a callback to handle the result after the algorithm completes
        def on_algorithm_complete(result):
            # Extract path and cumulative weight
            path = result.get("solution")
            weight = result.get("weight")

            if path:
                # Initialize the game state with the loaded grid, weights, and solution path
                self.gameState = GameState(
                    screen_width=self.SCREEN_WIDTH_GAME,
                    screen_height=self.SCREEN_HEIGHT_GAME,
                    rows=len(initial_grid),
                    columns=len(initial_grid[0]) if initial_grid else 0,
                    grid=initial_grid,
                    stone_weights=stone_weights,
                    path=path
                )
                # Set the game mode
                self.gameMode = PlayGameMode(self, self.gameState)
            else:
                print("No solution found")

        # Define the worker function to run the algorithm in a separate thread
        def algorithm_worker():
            # Read map and weights from the file
            if 1 <= level <= 9:
                initial_grid, stone_weights = read_level(f"input-0{level}.txt")
            else:
                initial_grid, stone_weights = read_level("input-10.txt")

            # Convert grid to tuple format if needed
            initial_grid = turnIntoTuple(initial_grid)

            # Initialize the problem
            problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)

            # Run the chosen algorithm
            if algo == "BFS":
                result = breadth_first_search(problem)
            elif algo == "DFS":
                result = depth_first_search(problem)
            elif algo == "UCS":
                result = uniform_cost_search(problem)
            elif algo == "A*":
                result = best_first_search(problem, lambda node: f(node))
            
            # Call the callback function with the result once done
            on_algorithm_complete(result)

        # Start the algorithm in a new thread
        threading.Thread(target=algorithm_worker, daemon=True).start()

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
            time_delta = self.clock.tick(60) / 1000.0
            
        pygame.quit()

    def applicationExit(self):
        self.running = False

userInterface = UserInterface()
userInterface.run()
