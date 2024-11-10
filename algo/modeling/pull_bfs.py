from collections import deque

import sys
INT_MAX = int(sys.maxsize // 100)
# INT_MAX = 4294967295

class pull_bfs:
    def __init__(self, switch_position, grid, ares_position):
        self.switch_position = switch_position
        self.grid = grid 
        self.ares_position = ares_position
        self.directions = [(-1, 0),(1, 0),(0, -1),(0, 1)]
        self.r_directions = [(1, 0),(-1, 0),(0, 1),(0, -1)]
        
    def run(self):
        dist = [[[[INT_MAX for j in range(len(self.grid[i]))] for i in range(len(self.grid))] for y in range(len(self.grid[x]))] for x in range(len(self.grid))]
        ares = self.ares_position
        switch = self.switch_position
        dist[ares[0]][ares[1]][switch[0]][switch[1]] = 0
        queue = deque([(ares, switch)])
        while queue:
            ares, switch = queue.popleft()
            for i in range(4):
                dr, dc = self.directions[i]
                r_dr, r_dc = self.r_directions[i]
                new_ares = (ares[0] + dr, ares[1] + dc)
                back_ares = (ares[0] + r_dr, ares[1] + r_dc)
                if self.is_valid_position(new_ares):
                    # move to new position
                    if dist[new_ares[0]][new_ares[1]][switch[0]][switch[1]] > dist[ares[0]][ares[1]][switch[0]][switch[1]]:
                        dist[new_ares[0]][new_ares[1]][switch[0]][switch[1]] = dist[ares[0]][ares[1]][switch[0]][switch[1]]
                        queue.append((new_ares, switch))
                    # move to new position with pulling stone
                    if back_ares == switch:
                        if dist[new_ares[0]][new_ares[1]][ares[0]][ares[1]] > dist[ares[0]][ares[1]][switch[0]][switch[1]] + 1:
                            dist[new_ares[0]][new_ares[1]][ares[0]][ares[1]] = dist[ares[0]][ares[1]][switch[0]][switch[1]] + 1
                            queue.append((new_ares, ares))
        answer = [[0 for j in range(len(self.grid[i]))] for i in range(len(self.grid))]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                answer[x][y] = min(dist[i][j][x][y] for i in range(len(self.grid)) for j in range(len(self.grid[i])))
        return answer 

    def is_valid_position(self, position):
            # Check if position is within bounds and not a wall
            row, col = position
            return (0 <= row < len(self.grid) and
                    0 <= col < len(self.grid[row]) and
                    self.grid[row][col] != "#")