from modeling import Node, expand

def depth_first_search(problem):
    """Implements Depth-First Search (DFS) with Tree-Search."""

    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # If the initial state is the goal, return immediately
    if problem.goal_test(node.state):
        return node
    
    # Stack for DFS
    frontier = [(node, [node.state])]  # Stack of (node, path), path keeps track of visited states in current branch
    explored = set()  # Set of explored states
    explored.add(node.state)  # Mark the initial state as explored
    
    while frontier:
        # Get the node and the path (history of states)
        node, path = frontier.pop()
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            # Convert the state to a hashable type
            hash_code = s.__hash__()
            
            # If the goal state is reached, return the child node
            if problem.goal_test(s):
                return child
            
            # If the state is not explored, add it to the frontier
            if hash_code not in explored:
                frontier.append((child, path + [s]))
                explored.add(hash_code)
    
    return None  # Return failure if no solution is found
