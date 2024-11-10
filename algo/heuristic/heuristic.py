import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching

def h(node, problem):
    stone_positions = list(node.state.stone_weight_map.keys())
    switch_positions = list(node.state.switch_positions)
    # Calculate the weight matrix for the stone-switch pairs
    stone_positions = list(node.state.stone_weight_map.keys())
    weight_matrix = [[problem.switch_distance[i][stone[0]][stone[1]] for i in range(len(stone_positions))]  for stone in stone_positions]
    if len(stone_positions) == 1 and len(switch_positions) == 1:
        # Directly use the single value in 1x1 weight matrix
        total_matching_cost = weight_matrix[0][0]
    else:
        # Convert to csr_matrix and use min_weight_full_bipartite_matching for larger cases
        weight_matrix = csr_matrix(weight_matrix)
        row_ind, col_ind = min_weight_full_bipartite_matching(weight_matrix)
        total_matching_cost = weight_matrix[row_ind, col_ind].sum()

    # Return the heuristic
    return total_matching_cost

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node, problem):
    """
    Evaluation function for A* search. It combines the path cost and
    the heuristic value (number of misplaced stones).
    """
    return node.path_cost + h(node, problem)