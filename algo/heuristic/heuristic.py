import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching
import sys
INT_MAX = int(sys.maxsize // 100)

def h(node, problem):
    stone_positions = list(node.state.stone_weight_map.keys())
    switch_positions = list(node.state.switch_positions)
    # Calculate the weight matrix for the stone-switch pairs
    stone_positions = list(node.state.stone_weight_map.keys())
    weight_matrix = [[problem.switch_distance[i][stone[0]][stone[1]] * node.state.stone_weight_map.get(stone) for i in range(len(stone_positions))]  for stone in stone_positions]
    if len(stone_positions) == 1 and len(switch_positions) == 1:
        # Directly use the single value in 1x1 weight matrix
        total_matching_cost = weight_matrix[0][0]
    else:
        # Convert to csr_matrix and use min_weight_full_bipartite_matching for larger cases
        weight_matrix = csr_matrix(weight_matrix)
        row_ind, col_ind = min_weight_full_bipartite_matching(weight_matrix)
        total_matching_cost = min(weight_matrix[row_ind, col_ind].sum(), INT_MAX)
    # Return the heuristic
    if total_matching_cost < 0:
        print("cost matching âm kìa pé")
    return total_matching_cost + move_heuristic(node)

# Define the evaluation function f for A* (path_cost + heuristic)
def f(node, problem):
    """
    Evaluation function for A* search. It combines the path cost and
    the heuristic value (number of misplaced stones).
    """
    return node.path_cost + h(node, problem)

def find_ares(node):
    grid = node.state.grid # Get the map
    # Find Ares
    rows = len(grid)
    for r in range(rows):
        cols = len(grid[r])
        for c in range(cols):
            if grid[r][c] == '@' or grid[r][c] == '+':
                return (r, c)
    return None

def move_heuristic(node):
    ares_position = find_ares(node)
    stone_positions = list(node.state.stone_weight_map.keys())
    min_stone_distance = INT_MAX
    for stone in stone_positions:
        if min_stone_distance > manhattan_distance(ares_position, stone):
            min_stone_distance = manhattan_distance(ares_position, stone)

def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
