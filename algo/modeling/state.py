class State:
    def __init__(self, grid, stone_weight_map):
        """
        Initializes the State with the grid and the stone weight map.
        
        grid: a tuple of tuples representing the grid.
        stone_weight_map: a dictionary mapping stone positions (row, col) to their weights.
        """
        self.grid = grid  # The Sokoban grid layout
        self.stone_weight_map = stone_weight_map  # Maps stone positions to their weights

    def update_stone_position(self, old_position, new_position):
        """
        Updates the stone weight map by moving the stone from old_position to new_position.
        """
        stone_weight = self.stone_weight_map.pop(old_position)
        self.stone_weight_map[new_position] = stone_weight

    def __repr__(self):
        return f"State(grid={self.grid}, stone_weight_map={self.stone_weight_map})"
