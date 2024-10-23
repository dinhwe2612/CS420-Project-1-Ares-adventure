from modeling import Node, expand
from utils import PriorityQueue

def best_first_search(problem, f):
    """Implements Best-First Search using the evaluation function `f`."""
    
    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # Create a priority queue ordered by the evaluation function f
    frontier = PriorityQueue()
    frontier.put(node, f(node))
    
    # A lookup table to store reached nodes (i.e., visited states)
    reached = {problem.initial_state: node}
    
    while not frontier.is_empty():
        # Get the node with the lowest f value from the frontier
        node = frontier.get()
        
        # If the goal state is reached, return the node
        if problem.goal_test(node.state):
            return node
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            
            # Check if the new state has not been reached or has a lower path cost
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child  # Mark the state as reached with the new path cost
                frontier.put(child, f(child))  # Add the child to the frontier
    
    return None  # Return failure if no solution is found