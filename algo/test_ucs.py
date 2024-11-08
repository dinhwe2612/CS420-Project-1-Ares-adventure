from modeling.problem import SokobanProblem
from ucs import uniform_cost_search
from heuristic import f
from io_process import read_file
from io_process import turnIntoTuple

# Define the initial Sokoban state (grid layout)
initial_grid = (
    ('#', '#', '#', '#'),
    (' ', '@', ' ', '#'),
    (' ', '$', '.', '#'),
    ('#', '#', '#', '#')
)

# Define stone weights (one stone with weight 1)
stone_weights = [1]

initial_grid, stone_weights = read_file("level1.txt")
initial_grid = turnIntoTuple(initial_grid)

# Create the Sokoban problem instance
problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)

# Run UCS and get the result dictionary
result = uniform_cost_search(problem)

# Extract the solution node from the result
solution = result.get("solution")

# Print the solution if found, otherwise notify no solution
if solution:
    print("Solution found:", solution)
else:
    print("No solution found")

# Print additional metrics from the result
print("Nodes expanded:", result.get("nodes"))
print("Steps:", result.get("steps"))
print("Weight:", result.get("weight"))
print("Time (ms):", result.get("time_ms"))
print("Memory (MB):", result.get("memory_mb"))
