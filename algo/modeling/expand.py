from .node import Node
from algo.deadlocks import detect_deadlock
import sys

INT_MAX = sys.maxsize

def expand(problem, node):
    """Generates the child nodes for each valid action."""
    s = node.state
    for action in problem.actions(s):
        # Get the resulting state and cost after applying the action
        s_prime, action_cost = problem.result_and_cost(s, action)

        # Detect deadlock
        if detect_deadlock(s_prime): 
            continue
        
        stone_positions = list(node.state.stone_weight_map.keys())
        for stone in stone_positions:
            if min(problem.switch_distance[i][stone[0]][stone[1]] for i in range(len(problem.switch_distance))) == INT_MAX:
                continue

        # Calculate the cost of moving to the new state
        cost = node.path_cost + action_cost
        # Calculate the steps
        steps = node.num_steps + 1
        # Calculate the weight
        weight = node.total_weight + action_cost - 1
        # Calculate the depth
        depth = node.depth + 1
        # Yield a new node corresponding to the resulting state
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost, num_steps=steps, total_weight=weight, depth=depth)
