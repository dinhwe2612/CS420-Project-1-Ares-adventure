from algo import SokobanProblem
from algo import best_first_search
from algo import f
from algo import read_file
from algo import turnIntoTuple

# Define the initial Sokoban state (grid layout)
# initial_grid = (
#     ('#', '#', '#', '#', '#', '#', '#', '#', '#', '#'),
#     ('#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'),
#     ('#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', '#'),
#     ('#', ' ', ' ', ' ', '.', ' ', '.', ' ', ' ', '#'),
#     ('#', ' ', ' ', ' ', '@', ' ', ' ', ' ', ' ', '#'),
#     ('#', ' ', '$', ' ', ' ', '.', ' ', ' ', ' ', '#'),
#     ('#', '#', '#', '#', '#', '#', '#', '#', '#', '#')
# )

# Define stone weights
# stone_weights = [2, 3, 1]

# initial_grid, stone_weights = read_file("input/input-01.txt")
initial_grid, stone_weights = read_file("algo/test/test1.txt")
# initial_grid = turnIntoTuple(initial_grid)

# Create the Sokoban problem instance
problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)

# Validate map
is_valid = problem.isMapLegit(initial_grid)
if not is_valid:
    print("Invalid map")
    exit()

# Run Best-First Search using the heuristic function `f`
result = best_first_search(problem, lambda node: f(node, problem))

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
print("Time:", result.get("time_ms"))
print("Memory (MB):", result.get("memory_mb"))
