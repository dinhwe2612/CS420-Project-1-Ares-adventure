from .node import Node
from .state import State

class SokobanProblem:
    def __init__(self, initial_grid, stone_weights):
        """
        Initializes the Sokoban problem with an initial grid and stone weights.
        
        initial_grid: a tuple of tuples representing the grid (each tuple represents a row).
        stone_weights: a list of integers representing the weights of the stones in the grid,
                       ordered by their appearance from top to bottom and left to right.
        """
        # Create an initial state with the grid and the stone weights
        stone_weight_map = self.map_stone_weights(initial_grid, stone_weights)
        self.initial_state = State(initial_grid, stone_weight_map)

    def map_stone_weights(self, grid, stone_weights):
        """
        Maps each stone's initial position to its corresponding weight.
        This mapping remains unchanged even when stones move.
        """
        weight_map = {}
        stone_count = 0
        
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == '$' or cell == '*':  # If it's a stone
                    weight_map[(r, c)] = stone_weights[stone_count]
                    stone_count += 1
        
        return weight_map

    def actions(self, state):
        """Returns the possible actions for the player in the current state."""
        possible_actions = []
        player_pos = self.find_player(state.grid)

        # Check u
        if self.is_valid_move(state.grid, player_pos, (-1, 0))[0] and not self.is_valid_move(state.grid, player_pos, (-1, 0))[1]:
            possible_actions.append('u')
        # Check d
        if self.is_valid_move(state.grid, player_pos, (1, 0))[0] and not self.is_valid_move(state.grid, player_pos, (1, 0))[1]:
            possible_actions.append('d')
        # Check l
        if self.is_valid_move(state.grid, player_pos, (0, -1))[0] and not self.is_valid_move(state.grid, player_pos, (0, -1))[1]:
            possible_actions.append('l')
        # Check r
        if self.is_valid_move(state.grid, player_pos, (0, 1))[0] and not self.is_valid_move(state.grid, player_pos, (0, 1))[1]:
            possible_actions.append('r')
        # Check U
        if self.is_valid_move(state.grid, player_pos, (-1, 0))[1]:
            possible_actions.append('U')
        # Check D
        if self.is_valid_move(state.grid, player_pos, (1, 0))[1]:
            possible_actions.append('D')
        # Check L
        if self.is_valid_move(state.grid, player_pos, (0, -1))[1]:
            possible_actions.append('L')
        # Check R
        if self.is_valid_move(state.grid, player_pos, (0, 1))[1]:
            possible_actions.append('R')

        return possible_actions

    def find_player(self, grid):
        """Finds the player's position in the grid."""
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == '@' or cell == '+':  # '@' is Ares, '+' is Ares on a switch
                    return (r, c)
        return None

    def is_valid_move(self, grid, player_pos, move):
        """
        Checks if a move from the player's current position is valid.
        """
        r, c = player_pos
        dr, dc = move
        new_r, new_c = r + dr, c + dc

        # Check if the new position is within bounds
        if not (0 <= new_r < len(grid)) or not (0 <= new_c < len(grid[0])):
            return False, False  # Out of bounds

        # Check if the new position is a wall
        if grid[new_r][new_c] == '#':
            return False, False  # If it's a wall

        # Check if it's a stone ('$' or '*'), and if so, whether the stone can be pushed
        if grid[new_r][new_c] == '$' or grid[new_r][new_c] == '*':
            next_r, next_c = new_r + dr, new_c + dc
            # Check if the next position after the stone is within bounds
            if not (0 <= next_r < len(grid)) or not (0 <= next_c < len(grid[0])):
                return False, False  # Out of bounds
            # Check if the space ahead of the stone is free or a switch
            if grid[next_r][next_c] in (' ', '.'):
                return True, True  # Valid push of the stone
            return False, False  # Stone cannot be pushed
        return True, False  # Move is valid if it's not blocked

    def result(self, state, action):
        """Returns the new state after applying the given action (UP, DOWN, LEFT, RIGHT)."""
        new_grid = [list(row) for row in state.grid]  # Create a deep copy of the grid
        player_pos = self.find_player(new_grid)
        r, c = player_pos

        action = action.lower()  # Normalize the action to lowercase

        # Determine new player position based on the action
        if action == "u":
            dr, dc = -1, 0
        elif action == "d":
            dr, dc = 1, 0
        elif action == "l":
            dr, dc = 0, -1
        elif action == "r":
            dr, dc = 0, 1

        new_r, new_c = r + dr, c + dc

        # If moving onto a stone, move the stone
        if new_grid[new_r][new_c] == '$':
            stone_r, stone_c = new_r + dr, new_c + dc
            if new_grid[stone_r][stone_c] == '.':  # Handle if the stone's new position is on a switch
                new_grid[stone_r][stone_c] = '*'
            else:
                new_grid[stone_r][stone_c] = '$'  # Move the stone
            new_grid[new_r][new_c] = '@'  # Move player to the stone's original position
            state.update_stone_position((new_r, new_c), (stone_r, stone_c))  # Update the stone weight map
        elif new_grid[new_r][new_c] == '*':
            stone_r, stone_c = new_r + dr, new_c + dc
            new_grid[stone_r][stone_c] = '$'  # Move the stone
            new_grid[new_r][new_c] = '+'  # The player is now on the switch
            state.update_stone_position((new_r, new_c), (stone_r, stone_c))  # Update the stone weight map
        elif new_grid[new_r][new_c] == '.':
            new_grid[new_r][new_c] = '+'  # Move player to a switch
        else:
            new_grid[new_r][new_c] = '@'  # Move player to the new position

        # Handle player moving from a switch (from '+')
        if new_grid[r][c] == '+':
            new_grid[r][c] = '.'  # Leave switch behind
        else:
            new_grid[r][c] = ' '  # Otherwise, just a free space

        # Return a new State object with the updated grid and stone weight map
        return State(tuple(tuple(row) for row in new_grid), state.stone_weight_map.copy())

    def goal_test(self, state):
        """Tests whether the current state is a goal."""
        for r in range(len(state.grid)):
            for c in range(len(state.grid[r])):
                if state.grid[r][c] == '$':  # If a stone is not on a switch
                    return False
        return True

    def action_cost(self, state, action):
        """
        Calculate the cost of a given action.
        If a stone is moved, the cost is 1 plus the weight of the stone.
        """
        player_pos = self.find_player(state.grid)
        r, c = player_pos

        action = action.lower()  # Normalize the action to lowercase

        # Determine new player position based on the action
        if action == "u":
            dr, dc = -1, 0
        elif action == "d":
            dr, dc = 1, 0
        elif action == "l":
            dr, dc = 0, -1
        elif action == "r":
            dr, dc = 0, 1

        new_r, new_c = r + dr, c + dc

        # If the player is moving a stone, calculate the stone's weight using the stone weight map
        if state.grid[new_r][new_c] == '$' or state.grid[new_r][new_c] == '*':
            stone_weight = state.stone_weight_map.get((new_r, new_c), 0)  # Fetch weight using the map
            return 1 + stone_weight  # Base cost 1 + stone weight
        else:
            return 1  # If no stone is moved, the cost is just 1