from modeling.problem import SokobanProblem
from best_first_search import best_first_search
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def h(node):
    stone_positions = node.state.stone_weight_map.keys()
    switch_positions = node.state.switch_positions
    # 
    weight_matrix = [[manhattan_distance(stone_position, switch_position)*node.state.stone_weight_map.get(stone_position) for switch_position in switch_positions] for stone_position in stone_positions]
    weight_matrix = csr_matrix(weight_matrix)
    row_ind, col_ind = min_weight_full_bipartite_matching(weight_matrix)
    #
    for r, row in enumerate(node.state.grid):
        for c, cell in enumerate(row):
            if cell == '@' or cell == '+':  # '@' is Ares, '+' is Ares on a switch
                ares_position = (r, c)
    min_dist_switch = min(manhattan_distance(ares_position, switch_position) for switch_position in switch_positions)
    return weight_matrix[row_ind, col_ind].sum() + min_dist_switch

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node):
    """
    Evaluation function for A* search. It combines the path cost and
    the heuristic value (number of misplaced stones).
    """
    return node.path_cost + h(node)

def read_file(filename):
    initial_grid = []
    stone_weights = []

    with open(filename, 'r') as file:
        # Read the first line for stone weights
        weights_line = file.readline().strip()
        stone_weights = list(map(int, weights_line.split()))

        # Read the rest of the file for the grid
        for line in file:
            # Ignore empty lines and strip each line of excess spaces
            row = tuple(line.rstrip())
            if row:
                initial_grid.append(row)

    # Convert list of lists into a tuple of tuples
    initial_grid = tuple(initial_grid)
    return initial_grid, stone_weights

# filename = "../input/input-05.txt"
# initial_grid, stone_weights = read_file(filename)

# Define the initial Sokoban state (grid layout)
initial_grid = (
    ('#', '#', '#', '#', '#', '#', '#', '#', '#', '#'),
    ('#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'),
    ('#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', '#'),
    ('#', ' ', ' ', ' ', '.', ' ', '.', ' ', ' ', '#'),
    ('#', ' ', ' ', ' ', '@', ' ', ' ', ' ', ' ', '#'),
    ('#', ' ', '$', ' ', ' ', '.', ' ', ' ', ' ', '#'),
    ('#', '#', '#', '#', '#', '#', '#', '#', '#', '#')
)

# Define stone weights (one stone with weight 1)
stone_weights = [2, 3, 1]

# Create the Sokoban problem instance
problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)

is_valid = problem.isMapLegit(initial_grid)
if not is_valid:
    print("Invalid map")
    exit()

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
    # Print steps, total_weight, and path_cost
    print("Steps:", solution.num_steps)
    print("Total weight:", solution.total_weight)
    print("Path cost:", solution.path_cost)
else:
    print("No solution found")
