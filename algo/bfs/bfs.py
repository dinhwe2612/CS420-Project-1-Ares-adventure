from modeling import Node, expand
import queue

def breadth_first_search(problem):
    """Implements Breadth-First search."""
    
    # Create the initial node
    node = Node(state=problem.initial_state)
    
    if problem.goal_test(node.state):
        return node
    
    # Create a queue
    frontier = queue.Queue()
    frontier.put(node)
    
    # A lookup table to store reached nodes (i.e., visited states)
    reached = {problem.initial_state: node}
    
    while not frontier.empty():
        # Get the node 
        node = frontier.get()
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            
            # If the goal state is reached, return the child
            if problem.goal_test(s):
                return child
            
            # Check if the new state has not been reached or has a lower path cost
            if s not in reached:
                reached[s] = child  # Mark the state as reached with the new path cost
                frontier.put(child)  # Add the child to the frontier
    
    return None  # Return failure if no solution is found