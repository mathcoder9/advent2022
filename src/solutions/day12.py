from collections import deque


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day12.txt") as file:
            data = file.read().split("\n")

        self.rows = len(data)
        self.columns = len(data[0])
        self.grid = [[0]*self.columns for _ in range(self.rows)]
        self.start_set = []
        for i, line in enumerate(data):
            for j, letter in enumerate(line):
                if letter == "S":
                    self.start_set.append((i, j))
                    self.start = [(i, j)]
                    self.grid[i][j] = 0
                elif letter == "E":
                    self.end = [i, j]
                    self.grid[i][j] = 25
                else:
                    self.grid[i][j] = ord(letter) - ord("a")
                    if letter == "a":
                        self.start_set.append((i, j))

    def valid_position(self, i, j) -> bool:
        return 0 <= i < self.rows and 0 <= j < self.columns

    def valid_jump(self, currentVal, jumpVal) -> bool:
        return jumpVal <= 1 + currentVal

    def check_at_end(self, i, j) -> bool:
        return i == self.end[0] and j == self.end[1]

    def bfs(self, startSet) -> int:
        q = deque()
        for position in startSet:
            q.append(((position[0], position[1]), 0))

        visited = set()
        while q:
            position, current_count = q.popleft()
            if position in visited:
                continue
            visited.add(position)

            position_x, position_y = position

            for i, j in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                new_position_x = position_x + i
                new_position_y = position_y + j
                if self.valid_position(new_position_x, new_position_y):
                    if self.check_at_end(new_position_x, new_position_y):
                        return current_count + 1
                    if self.valid_jump(self.grid[position_x][position_y], self.grid[new_position_x][new_position_y]):
                        q.append(
                            ((new_position_x, new_position_y), current_count + 1))

        return -1

    def solve(self) -> None:
        self.sol1 = self.bfs(self.start)
        self.sol2 = self.bfs(self.start_set)

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
