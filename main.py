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
        self.SCREEN_HEIGHT_GAME = 600

        pygame.init()

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.gameState = None
        self.gameMode = MenuGameMode(self, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
        self.prevGameMode = None

        self.clock = pygame.time.Clock()
        self.running = True
        
    def loadPlayGameMode(self):
        self.gameMode = PlayGameMode(self, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.SCREEN_HEIGHT_GAME, self.SCREEN_WIDTH_GAME)

    def run_algorithm(self, grid, stone_weights, algo):
        # Define a callback to handle the result after the algorithm completes
        def on_algorithm_complete(result):
            # Extract path and cumulative weight
            path = result.get("solution")
            weight = result.get("weight")
            print(path, weight)
            self.gameMode.run_solutionPath(path, weight)

        # Define the worker function to run the algorithm in a separate thread
        def algorithm_worker(initial_grid, stone_weights, algo):
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
        threading.Thread(target=algorithm_worker, args=(grid, stone_weights, algo), daemon=True).start()

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
