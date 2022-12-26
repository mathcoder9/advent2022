from collections import defaultdict
import time
from typing import Dict, Generator, List, Tuple


class Solution:

    dir_check = {0: [lambda x, y: (x-1, y+1), lambda x, y: (x-1, y-1), lambda x, y: (x-1, y)],
                 1: [lambda x, y: (x+1, y-1), lambda x, y: (x+1, y+1), lambda x, y: (x+1, y)],
                 2: [lambda x, y: (x+1, y-1), lambda x, y: (x-1, y-1), lambda x, y: (x, y-1)],
                 3: [lambda x, y: (x+1, y+1), lambda x, y: (x-1, y+1), lambda x, y: (x, y+1)]
                 }

    jumps = {0: lambda x, y: (x-1, y),
             1: lambda x, y: (x+1, y),
             2: lambda x, y: (x, y-1),
             3: lambda x, y: (x, y+1)
             }

    terminate = False

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day23.txt") as file:
            data = file.read().split("\n")

        self.positions = set()
        for x, line in enumerate(data):
            for y, char in enumerate(line):
                if char == "#":
                    self.positions.add((x, y))
        self.order = 0

    def get_neighbours(self, x: int, y: int) -> Generator:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                yield (x+i, y+j)

    def evolve(self):
        jump_map = defaultdict(list)
        neighbour_cache = set()
        for x, y in self.positions:
            if (x, y) not in neighbour_cache:
                make_move = False
                for neighbour in self.get_neighbours(x, y):
                    if neighbour in self.positions:
                        make_move = True
                        neighbour_cache.add(neighbour)
                if not make_move:
                    continue

            dir = self.order
            for _ in range(4):
                if all(fun(x, y) not in self.positions for fun in self.dir_check[dir]):
                    proposed_move = self.jumps[dir](x, y)
                    jump_map[proposed_move].append((x, y))
                    break
                dir += 1
                dir %= 4

        if not jump_map:
            self.terminate = True
            return
        self.update_positions(jump_map)

    def update_positions(self, jump_map: Dict[Tuple[int], List[Tuple[int]]]) -> None:
        for key, value in jump_map.items():
            if len(value) != 1:
                continue
            self.positions.add(key)
            self.positions.remove(value[0])

    def solve(self) -> None:
        i = 0
        while True:
            i += 1
            self.sol2 += 1
            self.evolve()
            if i == 10:
                self.sol1 = (max(x[0] for x in self.positions) + 1 - min(x[0] for x in self.positions)) * \
                    (max(x[1] for x in self.positions) + 1 - min(x[1]
                                                                 for x in self.positions)) - len(self.positions)
            if self.terminate:
                break
            self.order += 1
            self.order %= 4

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
