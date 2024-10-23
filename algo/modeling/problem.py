from .node import Node

class SokobanProblem:
    def __init__(self, initial_state, stone_weights):
        """
        Initializes the Sokoban problem with an initial state and stone weights.
        
        initial_state: a tuple of tuples representing the grid (each tuple represents a row).
        stone_weights: a list of integers representing the weights of the stones in the grid,
                       ordered by their appearance from top to bottom and left to right.
        """
        self.initial_state = initial_state
        self.stone_weights = stone_weights
        self.stone_weight_map = self.map_stone_weights(initial_state, stone_weights)

    def map_stone_weights(self, state, stone_weights):
        """
        Maps each stone's initial position to its corresponding weight.
        This mapping remains unchanged even when stones move.
        """
        weight_map = {}
        stone_count = 0
        
        for r, row in enumerate(state):
            for c, cell in enumerate(row):
                if cell == '$' or cell == '*':  # If it's a stone
                    weight_map[(r, c)] = stone_weights[stone_count]
                    stone_count += 1
        
        return weight_map
    
    def update_stone_weight_map(self, old_position, new_position):
        """
        Updates the stone_weight_map by removing the old_position and
        adding the new_position with the same weight.
        
        old_position: tuple (row, col) of the stone's old position
        new_position: tuple (row, col) of the stone's new position
        """
        # Get the stone's weight from the old position
        stone_weight = self.stone_weight_map.pop(old_position)

        # Add a new mapping for the stone at the new position with the same weight
        self.stone_weight_map[new_position] = stone_weight

    def actions(self, state):
        """Returns the possible actions for the player."""
        possible_actions = []
        player_pos = self.find_player(state)

        # Check UP
        if self.is_valid_move(state, player_pos, (-1, 0)):
            possible_actions.append('UP')
        # Check DOWN
        if self.is_valid_move(state, player_pos, (1, 0)):
            possible_actions.append('DOWN')
        # Check LEFT
        if self.is_valid_move(state, player_pos, (0, -1)):
            possible_actions.append('LEFT')
        # Check RIGHT
        if self.is_valid_move(state, player_pos, (0, 1)):
            possible_actions.append('RIGHT')

        return possible_actions

    def find_player(self, state):
        """Finds the player's position in the grid."""
        for r, row in enumerate(state):
            for c, cell in enumerate(row):
                if cell == '@' or cell == '+':  # '@' is Ares, '+' is Ares on a switch
                    return (r, c)
        return None

    def is_valid_move(self, state, player_pos, move):
        """
        Checks if a move from the player's current position is valid.
        A move is valid if:
        - The new position is within bounds.
        - The space is free (' ' or '.').
        - A stone ('$' or '*') can be pushed if present.
        """
        r, c = player_pos
        dr, dc = move
        new_r, new_c = r + dr, c + dc

        # Check if the new position is within bounds
        if not (0 <= new_r < len(state)) or not (0 <= new_c < len(state[0])):
            return False  # Out of bounds

        # Check if the new position is a wall
        if state[new_r][new_c] == '#':
            return False  # If it's a wall

        # Check if it's a stone ('$' or '*'), and if so, whether the stone can be pushed
        if state[new_r][new_c] == '$' or state[new_r][new_c] == '*':
            next_r, next_c = new_r + dr, new_c + dc
            # Check if the next position after the stone is within bounds
            if not (0 <= next_r < len(state)) or not (0 <= next_c < len(state[0])):
                return False  # Out of bounds
            # Check if the space ahead of the stone is free or a switch
            if state[next_r][next_c] in (' ', '.'):
                return True  # Valid push of the stone
            return False  # Stone cannot be pushed
        return True  # Move is valid if it's not blocked


    def result(self, state, action):
        """Returns the new state after applying the given action (UP, DOWN, LEFT, RIGHT)."""
        new_state = [list(row) for row in state]  # Create a deep copy of the state
        player_pos = self.find_player(state)
        r, c = player_pos

        # Determine new player position based on the action
        if action == "UP":
            dr, dc = -1, 0
        elif action == "DOWN":
            dr, dc = 1, 0
        elif action == "LEFT":
            dr, dc = 0, -1
        elif action == "RIGHT":
            dr, dc = 0, 1

        new_r, new_c = r + dr, c + dc

        # If moving onto a stone, move the stone
        if new_state[new_r][new_c] == '$':
            stone_r, stone_c = new_r + dr, new_c + dc
            if new_state[stone_r][stone_c] == '.':  # Handle if the stone's new position is on a switch
                new_state[stone_r][stone_c] = '*'
            else:
                new_state[stone_r][stone_c] = '$'  # Move the stone
            new_state[new_r][new_c] = '@'  # Move player to the stone's original position
            self.update_stone_weight_map((new_r, new_c), (stone_r, stone_c)) # Update the stone weight map
        elif new_state[new_r][new_c] == '*':
            stone_r, stone_c = new_r + dr, new_c + dc
            new_state[stone_r][stone_c] = '$'  # Move the stone
            new_state[new_r][new_c] = '+'  # The player is now on the switch
            self.update_stone_weight_map((new_r, new_c), (stone_r, stone_c)) # Update the stone weight map
        elif new_state[new_r][new_c] == '.':
            new_state[new_r][new_c] = '+'  # Move player to a switch
        else:
            new_state[new_r][new_c] = '@'  # Move player's to new position
        
        # Handle player moving from a switch (from '+')
        if new_state[r][c] == '+':
            new_state[r][c] = '.'  # Leave switch behind
        else:
            new_state[r][c] = ' '  # Otherwise, just a free space

        return tuple(tuple(row) for row in new_state)

    def goal_test(self, state):
        """Tests whether the current state is a goal."""
        for r in range(len(state)):
            for c in range(len(state[r])):
                if state[r][c] == '$':  # If a stone is not on a switch
                    return False
        return True

    def action_cost(self, state, action):
        """
        Calculate the cost of a given action.
        If a stone is moved, the cost is 1 plus the weight of the stone.
        """
        player_pos = self.find_player(state)
        r, c = player_pos

        # Determine new player position based on the action
        if action == "UP":
            dr, dc = -1, 0
        elif action == "DOWN":
            dr, dc = 1, 0
        elif action == "LEFT":
            dr, dc = 0, -1
        elif action == "RIGHT":
            dr, dc = 0, 1

        new_r, new_c = r + dr, c + dc

        # If the player is moving a stone, calculate the stone's weight using the initial mapping
        if state[new_r][new_c] == '$' or state[new_r][new_c] == '*':
            stone_weight = self.stone_weight_map.get((new_r, new_c), 0)  # Fetch weight using initial position
            return 1 + stone_weight  # Base cost 1 + stone weight
        else:
            return 1  # If no stone is moved, the cost is just 1

