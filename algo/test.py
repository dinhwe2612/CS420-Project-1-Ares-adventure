from modeling import SokobanProblem
from best_first_search import best_first_search

# Define a heuristic function h (for example, it can be the number of misplaced stones)
def h(node):
    # A simple heuristic: count the number of stones not on a switch
    state = node.state
    misplaced_stones = 0
    for row in state:
        misplaced_stones += row.count('$')  # Count all stones not placed on switches
    return misplaced_stones

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node):
    return node.path_cost + h(node)

# Define the initial Sokoban state
initial_state = (
    ('#', '#', '#', '#'),
    ('#', '@', ' ', '#'),
    ('#', '$', '.', '#'),
    ('#', '#', '#', '#')
)

# Define stone weights
stone_weights = [1]

# Create the Sokoban problem instance
problem = SokobanProblem(initial_state=initial_state, stone_weights=stone_weights)

# Run Best-First Search using a heuristic function
solution = best_first_search(problem, lambda node: f(node))

# Print the solution
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

