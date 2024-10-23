from modeling.problem import SokobanProblem
from best_first_search import best_first_search

# Define a heuristic function h (for example, it can be the number of misplaced stones)
def h(node):
    """
    Heuristic function that counts the number of misplaced stones
    (i.e., stones that are not on switches).
    """
    state = node.state
    grid = state.grid
    misplaced_stones = 0
    for row in grid:
        misplaced_stones += row.count('$')  # Count all stones not placed on switches
    return misplaced_stones

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node):
    """
    Evaluation function for A* search. It combines the path cost and
    the heuristic value (number of misplaced stones).
    """
    return node.path_cost + h(node)

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

# Run Best-First Search using A* with a heuristic function
solution = best_first_search(problem, lambda node: f(node))

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
