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