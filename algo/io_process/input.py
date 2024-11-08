def read_file(filename):
    initial_grid = []
    stone_weights = []

    with open(filename, 'r') as file:
        # Read the first line for stone weights
        weights_line = file.readline().strip()
        stone_weights = list(map(int, weights_line.split()))

        # Read the rest of the file for the grid
        for line in file:
            # Ignore empty lines and strip each line of excess spaces
            row = tuple(line.rstrip())
            if row:
                initial_grid.append(row)

    # Convert list of lists into a tuple of tuples
    initial_grid = tuple(initial_grid)
    return initial_grid, stone_weights

def read_level(filename):
    initial_grid = []
    stone_weights = []

    with open(filename, 'r') as file:
        # Read the first line for stone weights
        weights_line = file.readline().strip()
        stone_weights = list(map(int, weights_line.split()))

        # Read the rest of the file for the grid
        for line in file:
            # Ignore empty lines and strip each line of excess spaces
            row = list(line.rstrip())  # Use list instead of tuple for loadPlayGameMode compatibility
            if row:
                initial_grid.append(row)

    return initial_grid, stone_weights

def turnIntoTuple(grid):
    return tuple(tuple(row) for row in grid)
