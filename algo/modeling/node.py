class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state  # The state to which the node corresponds
        self.parent = parent  # The parent node that generated this node
        self.action = action  # The action taken to generate this node
        self.path_cost = path_cost  # The cost from the initial state to this node

    def __repr__(self):
        return f"Node(state={self.state}, parent={self.parent}, action={self.action}, path_cost={self.path_cost})"
