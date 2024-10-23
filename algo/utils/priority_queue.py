import heapq

class PriorityQueue:
    """Priority Queue implementation using heapq to support the frontier in BFS."""
    
    def __init__(self):
        self.elements = []
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]  # Returns the item with the lowest priority