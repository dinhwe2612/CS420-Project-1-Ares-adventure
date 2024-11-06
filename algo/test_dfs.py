from modeling.problem import SokobanProblem
from dfs import depth_first_search

# Define the initial Sokoban state (grid layout)
initial_grid = (
    ('#', '#', '#', '#'),
    (' ', '@', ' ', '#'),
    (' ', '$', '.', '#'),
    ('#', '#', '#', '#')
)

# Define stone weights (one stone with weight 1)
stone_weights = [1]

# Create the Sokoban problem instance
problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)

# Run BFS
solution = depth_first_search(problem)

# Print the solution if found, otherwise notify no solution
if solution:
    actions = []
    node = solution
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()  # Reverse the action list to get the correct order
    print("Solution found:", actions)
else:
    print("No solution found")
