from modeling import Node, expand

def depth_first_search(problem):
    """Implements Depth-First Search (DFS) with Tree-Search."""

    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # If the initial state is the goal, return immediately
    if problem.goal_test(node.state):
        return node
    
    # Stack for DFS (LIFO behavior)
    frontier = [(node, [node.state])]  # Stack of (node, path), path keeps track of visited states in current branch
    
    while frontier:
        # Get the node and the path (history of states)
        node, path = frontier.pop()
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            
            # If the goal state is reached, return the child node
            if problem.goal_test(s):
                return child
            
            # Check if the new state has been visited in this path (to prevent cycles)
            if s not in path:
                # Add the child node to the frontier and append current state to the path
                frontier.append((child, path + [s]))  # New path includes the current state
    
    return None  # Return failure if no solution is found
