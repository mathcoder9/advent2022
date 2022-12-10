from __future__ import annotations
from typing import List


class Solution:

    direction_map = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day9.txt") as file:
            self.data = [line.split(" ")
                         for line in file.read().split("\n")]

    def helper(self, number_of_knots) -> int:
        knots = [[0, 0] for _ in range(number_of_knots)]
        visited = {(0, 0)}

        for direction, steps in self.data:
            x, y = self.direction_map[direction]
            for _ in range(int(steps)):
                knots[0][0] += x
                knots[0][1] += y

                for i in range(1, number_of_knots):
                    knots[i] = self.update(knots[i-1], knots[i])

                visited.add(tuple(knots[-1]))

        return len(visited)

    def update(self, pointA, pointB) -> List[int]:
        if self.get_L1_distance(pointA, pointB) == 2:
            if pointA[0] == pointB[0]:
                pointB[1] += 1 if pointA[1] > pointB[1] else -1
            elif pointA[1] == pointB[1]:
                pointB[0] += 1 if pointA[0] > pointB[0] else -1
            else:
                pointB[0] += 1 if pointA[0] > pointB[0] else -1
                pointB[1] += 1 if pointA[1] > pointB[1] else -1

        return pointB

    def get_L1_distance(self, pointA, pointB) -> int:
        return max(abs(pointA[0]-pointB[0]), abs(pointA[1]-pointB[1]))

    def solve(self) -> None:
        self.sol1 = self.helper(2)
        self.sol2 = self.helper(10)

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
