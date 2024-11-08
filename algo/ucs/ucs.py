import time
import tracemalloc
from modeling import Node, expand
from utils import PriorityQueue
from best_first_search import best_first_search

# Define the evaluation function f for UCS (just the path_cost for UCS)
def f(node):
    """Evaluation function for UCS."""
    return node.path_cost

def uniform_cost_search(problem):
    return best_first_search(problem, lambda node: f(node))
