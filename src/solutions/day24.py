from collections import deque
from math import gcd
import time
from typing import Tuple


class Solution:

    char_change = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0)
    }

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.init_blizzard_cache()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day24.txt") as file:
            self.data = file.read().split("\n")

        self.row_length = len(self.data)
        self.col_length = len(self.data[0])
        self.lcm = ((self.row_length - 2) * (self.col_length - 2)
                    ) // gcd(self.row_length - 2, self.col_length - 2)

    def init_blizzard_cache(self) -> None:
        self.blizzard_cache = [set() for _ in range(self.lcm)]
        for row, line in enumerate(self.data):
            for col, char in enumerate(line):
                if char in [">", "<", "v", "^"]:
                    if char == ">":
                        for idx in range(self.lcm):
                            self.blizzard_cache[idx].add((row, col))
                            col += 1
                            if col == self.col_length - 1:
                                col = 1
                    elif char == "<":
                        for idx in range(self.lcm):
                            self.blizzard_cache[idx].add((row, col))
                            col -= 1
                            if col == 0:
                                col = self.col_length - 2
                    elif char == "^":
                        for idx in range(self.lcm):
                            self.blizzard_cache[idx].add((row, col))
                            row -= 1
                            if row == 0:
                                row = self.row_length - 2
                    elif char == "v":
                        for idx in range(self.lcm):
                            self.blizzard_cache[idx].add((row, col))
                            row += 1
                            if row == self.row_length - 1:
                                row = 1

    def is_valid(self, x: int, y: int) -> bool:
        return (x == 0 and y == 1) or (x == self.row_length - 1 and y == self.col_length - 2) or (1 <= x <= self.row_length - 2 and 1 <= y <= self.col_length - 2)

    def helper(self, start: Tuple(int), goal: Tuple(int), time: int) -> int:
        q = deque([start])
        minutes = time

        while q:
            minutes += 1
            blizzard = self.blizzard_cache[minutes % self.lcm]
            processed = set()
            for _ in range(len(q)):
                x, y = q.popleft()

                for a, b in [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]:
                    new_x, new_y = x+a, y+b
                    if not self.is_valid(new_x, new_y):
                        continue

                    if (new_x, new_y) == goal:
                        return minutes

                    if (new_x, new_y) in blizzard:
                        continue

                    if (new_x, new_y) in processed:
                        continue
                    processed.add((new_x, new_y))

                    q.append((new_x, new_y))

        return -1

    def solve(self) -> None:
        t1 = self.helper((0, 1), (self.row_length - 1, self.col_length - 2), 0)
        t2 = self.helper(
            (self.row_length - 1, self.col_length - 2), (0, 1), t1)
        t3 = self.helper((0, 1), (self.row_length -
                         1, self.col_length - 2), t2)

        self.sol1 = t1
        self.sol2 = t3

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
