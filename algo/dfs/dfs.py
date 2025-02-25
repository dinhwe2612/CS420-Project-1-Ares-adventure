import time
import psutil
# import tracemalloc
from algo.modeling import Node, expand

def depth_first_search(problem):
    """Implements Depth-First Search with node, time, specific memory, steps, and weight tracking."""

    # Track performance metrics
    start_time = time.perf_counter()

    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # If the initial state is the goal, return immediately
    if problem.goal_test(node.state):
        total_time_ms = (time.perf_counter() - start_time)*1000
        memory_usage = psutil.Process().memory_info().rss
        
        return {
            "solution": [],
            "nodes": 0,
            "steps": 0,
            "weight": 0,
            "time_ms": round(total_time_ms, 2),
            "memory_mb": round(memory_usage / (1024 * 1024), 2)
        }
    
    # Stack for DFS
    frontier = [(node, [node.state])]  # Stack of (node, path)
    hash_code = node.state.__hash__()
    explored = set()  # Set of explored states
    explored.add(hash_code)
    
    # Track the number of nodes expanded
    nodes_expanded = 0
    
    while frontier:
        # Get the node and path (history of states)
        node, path = frontier.pop()
        nodes_expanded += 1  # Count each node expanded

        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            hash_code = s.__hash__()
            
            # If the goal state is reached, collect metrics and return results
            if problem.goal_test(s):
                total_time_ms = (time.perf_counter() - start_time)
                memory_usage = psutil.Process().memory_info().rss
                
                # Calculate steps and weight
                actions = []
                weight = []
                current = child
                while current.parent is not None:
                    actions.append(current.action)
                    weight.append(current.path_cost)
                    current = current.parent

                actions.reverse()  # Reverse the action list to get the correct order
                actions = ''.join(actions)
                weight.reverse()
                
                return {
                    "solution": actions,
                    "nodes": nodes_expanded,
                    "steps": child.num_steps,
                    "weight": weight,
                    "time_ms": round(total_time_ms, 2)*1000,
                    "memory_mb": round(memory_usage / (1024 * 1024), 2)
                }
            
            # If the state has not been explored, add it to the frontier
            if hash_code not in explored:
                frontier.append((child, path + [s]))
                explored.add(hash_code)
    
    # Return metrics if no solution is found
    total_time_ms = (time.perf_counter() - start_time)
    memory_usage = psutil.Process().memory_info().rss
    
    return {
        "solution": None,
        "nodes": nodes_expanded,
        "steps": 0,
        "weight": 0,
        "time_ms": round(total_time_ms, 2)*1000,
        "memory_mb": round(memory_usage / (1024 * 1024), 2)
    }
