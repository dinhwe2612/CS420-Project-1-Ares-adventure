# import time
# import tracemalloc
from algo.modeling import Node, expand
from algo.utils import PriorityQueue
import time
import psutil

def best_first_search(problem, f):
    """Implements Best-First Search with node, time, specific memory, steps, and weight tracking."""

    # Track performance metrics
    start_time = time.perf_counter()
    
    # # Start memory tracking with tracemalloc
    # tracemalloc.start()
    
    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # Create a priority queue ordered by the evaluation function f
    frontier = PriorityQueue()
    frontier.put(node, f(node))
    
    # Track the number of nodes expanded
    nodes_expanded = 0
    reached = {hash(problem.initial_state): node}
    
    while not frontier.is_empty():
        # Get the node with the lowest f value from the frontier
        node = frontier.get()
        nodes_expanded += 1  # Count each node expanded
        
        # If the goal state is reached, collect metrics and return results
        if problem.goal_test(node.state):
            # end_time = time.time()
            # total_time_ms = (end_time - start_time) * 1000
            time_elapsed = (time.perf_counter() - start_time)
            # _, peak_memory = tracemalloc.get_traced_memory()
            # tracemalloc.stop()
            memory_usage = psutil.Process().memory_info().rss
            
            # Calculate steps by tracing back from the goal node to the root
            actions = []
            weight = []
            current = node
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
                "steps": node.num_steps,
                "weight": weight,
                "time_ms": time_elapsed*1000,
                "memory_mb": (round(memory_usage / (1024 * 1024), 2))
                # "time_ms": round(total_time_ms, 2),
                # "memory_mb": round(peak_memory / (1024 * 1024), 2)
            }
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            s_hash = hash(s)  # Get the hash of the state
            
            # Check if the new state has not been reached or has a lower path cost
            if s_hash not in reached or child.path_cost < reached[s_hash].path_cost:
                reached[s_hash] = child  # Mark the state as reached with the new path cost
                frontier.put(child, f(child))  # Add the child to the frontier
    
    # Return metrics if no solution is found
    # end_time = time.time()
    # total_time_ms = (end_time - start_time) * 1000
    # _, peak_memory = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    time_elapsed = (time.perf_counter() - start_time)
            # _, peak_memory = tracemalloc.get_traced_memory()
            # tracemalloc.stop()
    memory_usage = psutil.Process().memory_info().rss

    print(node.state)
    
    return {
        "solution": None,
        "nodes": nodes_expanded,
        "steps": 0,
        "weight": 0,
        "time_ms": time_elapsed*1000,
        "memory_mb": (round(memory_usage / (1024 * 1024), 2))
        # "time_ms": round(total_time_ms, 2),
        # "memory_mb": round(peak_memory / (1024 * 1024), 2)
    }
