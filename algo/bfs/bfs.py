from modeling import Node, expand
import queue
import time
# import tracemalloc
import psutil

def breadth_first_search(problem):
    """Implements Breadth-First Search with node, time, specific memory, steps, and weight tracking."""
    
    # Track performance metrics
    # start_time = time.time()
    start_time = time.perf_counter()
    
    # Start memory tracking with tracemalloc
    # tracemalloc.start()
    
    # Create the initial node
    node = Node(state=problem.initial_state)
    
    # If the initial state is the goal, return immediately
    if problem.goal_test(node.state):
        # end_time = time.time()
        # total_time_ms = (end_time - start_time) * 1000
        # _, peak_memory = tracemalloc.get_traced_memory()
        # tracemalloc.stop()  # Stop tracemalloc to avoid further tracking
        time_elapsed = (time.perf_counter() - start_time)
            # _, peak_memory = tracemalloc.get_traced_memory()
            # tracemalloc.stop()
        memory_usage = psutil.Process().memory_info().rss
        return {
            "solution": [],
            "nodes": 0,
            "steps": 0,
            "weight": 0,
            "time_ms": round(time_elapsed, 2)*1000,
            "memory_mb": round(memory_usage / (1024 * 1024), 2)  # Convert bytes to MB
        }
    
    # Create a queue and add the initial node
    frontier = queue.Queue()
    frontier.put(node)
    
    # Track the number of nodes expanded
    nodes_expanded = 0
    reached = {hash(problem.initial_state): node}
    
    # Main search loop
    while not frontier.empty():
        node = frontier.get()
        nodes_expanded += 1  # Count each node expanded
        
        # Expand the current node
        for child in expand(problem, node):
            s = child.state
            s_hash = hash(s)  # Get the hash of the state
            
            # If the goal state is reached, collect metrics and return results
            if problem.goal_test(s):
                # end_time = time.time()
                # total_time_ms = (end_time - start_time) * 1000
                # _, peak_memory = tracemalloc.get_traced_memory()
                # tracemalloc.stop()  # Stop tracemalloc
                total_time_ms = (time.perf_counter() - start_time)
                memory_usage = psutil.Process().memory_info().rss

                # Calculate steps by tracing back from the goal node to the root
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
            
            # Check if the state has not been reached before
            if s_hash not in reached:
                reached[s_hash] = child
                frontier.put(child)
    
    # Return metrics if no solution is found
    end_time = time.time()
    total_time_ms = (time.perf_counter() - start_time)*1000
    memory_usage = psutil.Process().memory_info().rss  # Stop tracemalloc
    
    return {
        "solution": None,
        "nodes": nodes_expanded,
        "steps": 0,
        "weight": 0,
        "time_ms": round(total_time_ms, 2)*1000,
        "memory_mb": round(memory_usage / (1024 * 1024), 2)
    }
