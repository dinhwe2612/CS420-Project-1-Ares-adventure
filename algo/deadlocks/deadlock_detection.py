import sys
INT_MAX = int(sys.maxsize // 100)

def is_in_corner(grid, pos):
    """
    Checks if a stone is in a corner, which would cause a deadlock unless it’s already on a goal.
    """
    r, c = pos
    if grid[r][c] != '$':
        return False

    # Corner conditions (both adjacent cells are walls)
    return (
        (grid[r-1][c] == '#' and grid[r][c-1] == '#') or
        (grid[r-1][c] == '#' and grid[r][c+1] == '#') or
        (grid[r+1][c] == '#' and grid[r][c-1] == '#') or
        (grid[r+1][c] == '#' and grid[r][c+1] == '#')
    )

def is_on_border_between_corners(grid, pos):
    """
    Checks if a stone is on a border between two corners, causing a deadlock if it cannot be moved.
    """
    r, c = pos
    # Detect horizontal or vertical wall-adjacent positions with obstacles on both sides
    if grid[r][c] != '$':
        return False
    return (
        (grid[r][c-1] == '#' and grid[r][c+1] == '#') or
        (grid[r-1][c] == '#' and grid[r+1][c] == '#')
    )

def detect_two_stone_deadlock(grid):
    """
    Detects deadlocks with two stones positioned along a wall where both cannot be moved.
    """
    rows = len(grid)
    for r in range(rows):
        cols = len(grid[r])
        for c in range(cols):
            # Check if current cell and its neighbor contain stones along a wall
            if grid[r][c] == '$' and grid[r][c + 1] == '$':
                # Stones side-by-side along a horizontal wall
                if grid[r - 1][c] == '#' and grid[r - 1][c + 1] == '#':
                    return True
                if grid[r + 1][c] == '#' and grid[r + 1][c + 1] == '#':
                    return True
            elif grid[r][c] == '$' and grid[r + 1][c] == '$':
                # Stones stacked vertically along a wall
                if grid[r][c - 1] == '#' and grid[r + 1][c - 1] == '#':
                    return True
                if grid[r][c + 1] == '#' and grid[r + 1][c + 1] == '#':
                    return True
    return False

def retrieve_stone_positions(grid):
    """
    Retrieves positions of all stones from the grid.

    Parameters:
    - grid: a 2D tuple representing the current grid state.

    Returns:
    - list of tuples: List of (row, col) positions where stones are located.
    """
    stone_positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '$' or cell == '*':  # Stone or stone on a switch
                stone_positions.append((r, c))
    return stone_positions

def detect_deadlock(problem, state):
    """
    Detects if the current state has reached a deadlock configuration where it
    becomes impossible to reach the goal.

    Parameters:
    - state: State object representing the current grid and positions.

    Returns:
    - bool: True if the state is a deadlock, False otherwise.
    """

    # Retrieve stone positions directly from the grid
    stone_positions = retrieve_stone_positions(state.grid)
    for pos in stone_positions:
        if pos in problem.dead_square:
            return True

    # Check for simple deadlock patterns (e.g., stones in corners)
    for stone_pos in stone_positions:
        if is_in_corner(state.grid, stone_pos):
            # print("Is in corner")
            return True

    # Check for two-stone deadlocks along walls
    if detect_two_stone_deadlock(state.grid):
        # print("Two stone deadlock")
        return True

    # Check for "L"-shaped deadlocks with three stones
    if detect_three_stone_L_deadlock(state.grid):
        # print("Three stone L deadlock")
        return True

    # Check for frozen deadlocks
    if detect_frozen_deadlock(state.grid, stone_positions):
        # print("Frozen deadlock")
        return True

    return False

def detect_three_stone_L_deadlock(grid):
    """
    Detects three-stone deadlocks in an L shape where they block each other.
    """
    rows = len(grid)
    for r in range(rows - 1):
        cols = len(grid[r])
        for c in range(cols - 1):
            # Check if there is an "L" shape with stones at (r, c), (r+1, c), and (r, c+1)
            if (grid[r][c] == '$' and grid[r+1][c] == '$' and grid[r][c+1] == '$'):
                if grid[r+1][c+1] == '#':  # Bottom-right corner blocked
                    return True
            # Check if there is an "L" shape with stones at (r, c+1), (r+1, c+1), and (r, c)
            elif (grid[r][c+1] == '$' and grid[r+1][c+1] == '$' and grid[r][c] == '$'):
                if grid[r+1][c] == '#':  # Bottom-left corner blocked
                    return True
    return False

def detect_frozen_deadlock(grid, stone_positions):
    """
    Detects frozen deadlocks where stones are surrounded by walls or other stones and cannot move.
    """
    for pos in stone_positions:
        r, c = pos
        if (is_surrounded_by_walls_or_stones(grid, r, c)):
            return True
    return False

def is_surrounded_by_walls_or_stones(grid, r, c):
    """
    Checks if a stone at position (r, c) is surrounded by walls or other stones.
    """
    surrounding = [
        grid[r-1][c] if r > 0 else '#',
        grid[r+1][c] if r < len(grid) - 1 else '#',
        grid[r][c-1] if c > 0 else '#',
        grid[r][c+1] if c < len(grid[r]) - 1 else '#'
    ]
    return all(cell == '#' or cell == '$' for cell in surrounding)
        
# Tutorial: goals: set of goals, walls: set of walls, paths: anything except walls 
# directions = [u, d, l, r]
# dead_squuare is a set of cells that will cause deadlock

# def set_distance():
# 	distanceToGoal = dict()
# 	dead_squares = set()
# 	for goal in goals:
# 		distanceToGoal[goal] = dict()
# 		for path in paths:
# 			distanceToGoal[goal][path] = 1e9
# 	queue = Queue()
# 	for goal in goals:
# 		distanceToGoal[goal][goal] = 0
# 		queue.put(goal)
# 		while not queue.empty():
# 			position = queue.get()
# 			for direction in directions:
# 				boxPosition = (position[0] + direction.vector[0], position[1] + direction.vector[1])
# 				playerPosition = (position[0] + 2*direction.vector[0], position[1] + 2*direction.vector[1])
# 				if boxPosition in paths:
# 					if distanceToGoal[goal][boxPosition] == 1e9:
# 						if (boxPosition not in walls) and (playerPosition not in walls):
# 							distanceToGoal[goal][boxPosition] = distanceToGoal[goal][position] + 1
# 							queue.put(boxPosition)
#
# 	for path in paths:
# 		ok = 1
# 		for goal in goals:	
# 			if distanceToGoal[goal][path] != 1e9:
# 				ok = 0
# 				break
# 		if ok == 1:
# 			dead_squares.add(path)
# 	return distanceToGoal, dead_squares