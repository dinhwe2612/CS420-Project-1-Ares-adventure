class State:
    def __init__(self, grid, stone_weight_map):
        """
        Initializes the State with the grid and the stone weight map.
        
        grid: a tuple of tuples representing the grid.
        stone_weight_map: a dictionary mapping stone positions (row, col) to their weights.
        """
        self.grid = grid  # The Sokoban grid layout
        self.stone_weight_map = stone_weight_map  # Maps stone positions to their weights
        self.switch_positions = self.find_switch_positions()

    def update_stone_position(self, old_position, new_position):
        """
        Updates the stone weight map by moving the stone from old_position to new_position.
        """
        if old_position in self.stone_weight_map:
            self.stone_weight_map[new_position] = self.stone_weight_map.pop(old_position)

    def __repr__(self):
        return f"State(grid={self.grid}, stone_weight_map={self.stone_weight_map})"
    
    def find_switch_positions(self):
        """
        Finds the positions of the switches in the grid.
        """
        switch_positions = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == '.' or self.grid[row][col] == '+' or self.grid[row][col] == '*':
                    switch_positions.append((row, col))
        return switch_positions
    def __hash__(self):
        # Iterate over the grid to create a hashable representation
        hashable = ()
        for row in self.grid:
            hashable += tuple(row)
        return hash(hashable)
