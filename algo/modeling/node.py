class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, num_steps=0, total_weight=0, depth = 0):
        self.state = state  # The State object (grid + stone weights)
        self.parent = parent  # The parent node that generated this node
        self.action = action  # The action taken to generate this node
        self.num_steps = num_steps  # The number of steps Ares has to take
        self.total_weight = total_weight  # The total weight Ares has to carry
        self.path_cost = path_cost  # The cost from the initial state to this node
        self.depth = depth # The depth of the node

    def __lt__(self, other):
        """Compares two nodes based on path cost (for priority queues)."""
        return self.path_cost < other.path_cost

    def __repr__(self):
        return f"Node(state={self.state}, parent={self.parent}, action={self.action}, path_cost={self.path_cost})"