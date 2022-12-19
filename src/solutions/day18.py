from collections import deque
from functools import lru_cache
import time
import sys


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day18.txt") as file:
            data = file.read().split("\n")
        self.droplet = set()
        for line in data:
            self.droplet.add(tuple([int(num) for num in line.split(",")]))

        self.constraints = []
        self.constraints.append((min(cube[0] for cube in self.droplet)-1, max(
            cube[0] for cube in self.droplet) + 1))
        self.constraints.append((min(cube[1] for cube in self.droplet)-1, max(
            cube[1] for cube in self.droplet) + 1))
        self.constraints.append((min(cube[2] for cube in self.droplet)-1, max(
            cube[2] for cube in self.droplet) + 1))

    def get_neighbours(self, cube):
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            yield (cube[0] + dx, cube[1] + dy, cube[2] + dz)

    def make_cast(self):

        def in_box(cube):
            return self.constraints[0][0] <= cube[0] <= self.constraints[0][1] and self.constraints[1][0] <= cube[1] <= self.constraints[1][1] and self.constraints[2][0] <= cube[2] <= self.constraints[2][1]

        q = deque(
            [(self.constraints[0][0], self.constraints[1][0], self.constraints[2][0])])

        cast = set()
        while q:
            cube = q.popleft()
            if cube in cast:
                continue
            cast.add(cube)

            for neighbour in self.get_neighbours(cube):
                if neighbour in self.droplet:
                    continue
                if in_box(neighbour):
                    q.append(neighbour)

        return cast

    def make_filled_droplet(self):
        cast = self.make_cast()
        return set([(i, j, k) for i in range(self.constraints[0][0], self.constraints[0][1] + 1) for j in range(
            self.constraints[1][0], self.constraints[1][1] + 1) for k in range(self.constraints[2][0], self.constraints[2][1] + 1)]) - cast

    def helper(self, droplet):
        area = 0
        for cube in droplet:
            for neighbour in self.get_neighbours(cube):
                area += neighbour not in droplet
        return area

    def solve(self):
        self.sol1 = self.helper(self.droplet)
        self.sol2 = self.helper(self.make_filled_droplet())

    def get_solution(self) -> int:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
