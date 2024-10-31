from modeling.problem import SokobanProblem
from best_first_search import best_first_search

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def find_closest_switch(stone_position, switch_positions):
    closest_switch = switch_positions[0]
    min_distance = manhattan_distance(stone_position[0], stone_position[1], closest_switch[0], closest_switch[1])
    for switch_position in switch_positions[1:]:
        distance = manhattan_distance(stone_position[0], stone_position[1], switch_position[0], switch_position[1])
        if distance < min_distance:
            min_distance = distance
            closest_switch = switch_position
    return closest_switch

def h(node):
    stone_positions = node.state.stone_weight_map.keys()
    switch_positions = node.state.switch_positions
    total_distance = 0
    for stone_position in stone_positions:
        closest_switch = find_closest_switch(stone_position, switch_positions)
        total_distance += manhattan_distance(stone_position[0], stone_position[1], closest_switch[0], closest_switch[1]) * node.state.stone_weight_map[stone_position]
    return total_distance

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
    actions = ''.join(actions)
    print("Solution found:", actions)
else:
    print("No solution found")
