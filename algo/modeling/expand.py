from .node import Node

def expand(problem, node):
    """Generates the child nodes for each valid action."""
    s = node.state
    for action in problem.actions(s):
        # Get the resulting state after applying the action
        s_prime = problem.result(s, action)
        # Calculate the cost of moving to the new state
        cost = node.path_cost + problem.action_cost(s, action)
        # Yield a new node corresponding to the resulting state
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)