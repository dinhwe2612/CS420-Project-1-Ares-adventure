import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from .input import read_file
from algo.modeling import SokobanProblem
from algo.heuristic import f
from algo.bfs import breadth_first_search
from algo.dfs import depth_first_search
from algo.ucs import uniform_cost_search
from algo.best_first_search import best_first_search

def process_result(result):
    # Extract the solution node if found
    solution = result.get("solution")

    # Prepare the dictionary to store the result
    output = {
        "solution_found": False,
        "steps": None,
        "weight": None, 
        "nodes_expanded": result.get("nodes"),
        "time_ms": result.get("time_ms"),
        "memory_mb": result.get("memory_mb"),
        "actions": None,
    }

    # If solution is found, generate the action sequence
    if solution:
        output["solution_found"] = True
        output["actions"] = solution
        output["steps"] = result.get("steps")
        output["weight"] = result.get("weight")[-1]
    else:
        output["actions"] = "No solution found"
        output["steps"] = "No steps measured"
        output["weight"] = "No weight measured"

    return output

def format_result(algo_name, result):
    """
    Formats the result of an algorithm in the specified output format.
    """
    steps = result.get("steps", 0)
    weight = result.get("weight", 0)
    nodes = result.get("nodes", 0)
    time_ms = result.get("time_ms", 0.0)
    memory_mb = result.get("memory_mb", 0.0)
    solution = result.get("solution")

    # Print the solution if found, otherwise notify no solution
    if not solution:
        solution = "No solution found"
    
    # Construct the formatted result as a string
    formatted_result = [
        f"{algo_name}",
        f"Steps: {steps}, Weight: {weight}, Nodes: {nodes}, Time (ms): {time_ms}, Memory (MB): {memory_mb}",
        solution
    ]
    return "\n".join(formatted_result)

def generate_output_for_input_file(input_file):
    """
    Generates a single output file for a given input file by running four algorithms and
    saving all results to one output file.
    
    Parameters:
    - input_file (str): The path to the input file (e.g., 'input/input-01.txt').
    """
    # Extract the input file index from the filename for output naming
    input_index = int(os.path.basename(input_file).split('-')[1].split('.')[0])
    
    # Read initial grid and stone weights from the input file
    initial_grid, stone_weights = read_file(input_file)
    
    # Initialize Sokoban problem instance
    problem = SokobanProblem(initial_grid=initial_grid, stone_weights=stone_weights)
    
    # Directory for output files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    output_file = os.path.join(output_dir, f"output-{input_index:02}.txt")
    
    # Run each algorithm and collect results
    results = []

    # Run BFS
    try:
        bfs_result = breadth_first_search(problem)
        results.append(format_result("BFS", bfs_result))
        print(f"BFS completed successfully for input {input_index}.")
    except Exception as e:
        print(f"Error in BFS for input {input_index}: {e}")
        results.append(f"BFS\nError: {e}")

    # Run DFS
    try:
        dfs_result = depth_first_search(problem)
        results.append(format_result("DFS", dfs_result))
        print(f"DFS completed successfully for input {input_index}.")
    except Exception as e:
        print(f"Error in DFS for input {input_index}: {e}")
        results.append(f"DFS\nError: {e}")

    # Run UCS
    try:
        ucs_result = uniform_cost_search(problem)
        results.append(format_result("UCS", ucs_result))
        print(f"UCS completed successfully for input {input_index}.")
    except Exception as e:
        print(f"Error in UCS for input {input_index}: {e}")
        results.append(f"UCS\nError: {e}")

    # Run A*
    try:
        astar_result = best_first_search(problem, lambda node: f(node))
        results.append(format_result("A*", astar_result))
        print(f"A* completed successfully for input {input_index}.")
    except Exception as e:
        print(f"Error in A* for input {input_index}: {e}")
        results.append(f"A*\nError: {e}")

    # Write all results to a single output file
    with open(output_file, "w") as file:
        file.write("\n\n".join(results))  # Separate each algorithm result with a blank line
    
    print(f"All results written to {output_file}")
