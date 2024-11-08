import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def h(node):
    stone_positions = list(node.state.stone_weight_map.keys())
    switch_positions = list(node.state.switch_positions)

    # Calculate the weight matrix for the stone-switch pairs
    weight_matrix = [[manhattan_distance(stone_position, switch_position) * node.state.stone_weight_map.get(stone_position)
                      for switch_position in switch_positions] for stone_position in stone_positions]
    
    if len(stone_positions) == 1 and len(switch_positions) == 1:
        # Directly use the single value in 1x1 weight matrix
        total_matching_cost = weight_matrix[0][0]
    else:
        # Convert to csr_matrix and use min_weight_full_bipartite_matching for larger cases
        weight_matrix = csr_matrix(weight_matrix)
        row_ind, col_ind = min_weight_full_bipartite_matching(weight_matrix)
        total_matching_cost = weight_matrix[row_ind, col_ind].sum()

    # Calculate Ares' position and distance to the closest switch
    ares_position = next((r, c) for r, row in enumerate(node.state.grid) for c, cell in enumerate(row) if cell == '@' or cell == '+')
    min_dist_switch = min(manhattan_distance(ares_position, switch_position) for switch_position in switch_positions)

    # Return the heuristic
    return total_matching_cost + min_dist_switch

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node):
    """
    Evaluation function for A* search. It combines the path cost and
    the heuristic value (number of misplaced stones).
    """
    return node.path_cost + h(node)