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
