import time
from typing import Set, Tuple


class Solution:

    rocks = [[(2, 0), (3, 0), (4, 0), (5, 0)], [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)], [
        (2, 0), (3, 0), (4, 0), (4, 1), (4, 2)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(2, 0), (2, 1), (3, 0), (3, 1)]]

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.width = 7
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day17.txt") as file:
            self.data = file.read()

    def shift_rocks_left(self, rocks: Set[Tuple[int]], column: Set[Tuple[int]]) -> Set[Tuple[int]]:
        shifted_rocks = set([(rock[0]-1, rock[1])
                            for rock in rocks])
        if any(point[0] < 0 for point in shifted_rocks) or shifted_rocks & column:
            return rocks
        return shifted_rocks

    def shift_rocks_right(self, rocks: Set[Tuple[int]], column: Set[Tuple[int]]) -> Set[Tuple[int]]:
        shifted_rocks = set([(rock[0]+1, rock[1])
                            for rock in rocks])
        if any(point[0] >= self.width for point in shifted_rocks) or shifted_rocks & column:
            return rocks
        return shifted_rocks

    def shift_rocks_down(self, rocks: Set[Tuple[int]], column: Set[Tuple[int]]) -> Set[Tuple[int]]:
        shifted_rocks = set([(rock[0], rock[1]-1)
                            for rock in rocks])
        if shifted_rocks & column:
            return rocks
        return shifted_rocks

    # cycle detection is not the most rigorous. probably have to hash the column data as a key for general cases.
    def helper(self, count: int) -> int:
        column = set()
        for rock_num in range(7):
            column.add((rock_num, -1))
        n = len(self.data)
        floor_height = -1
        idx = 0
        cache = {}
        for rock_num in range(0, count):
            rocks = self.rocks[rock_num % 5]
            rock_height = floor_height + 4
            rock_set = set([(rock[0], rock_height + rock[1])
                            for rock in rocks])

            cache_key = (rock_num % 5, idx % n)

            if cache_key in cache:
                prev_rock_number, prev_floor_height = cache[cache_key]
                period = rock_num - prev_rock_number
                height = floor_height - prev_floor_height
                if count % period == rock_num % period:
                    return floor_height + \
                        ((count - rock_num)//period) * height + 1

            cache[cache_key] = (rock_num, floor_height)

            while True:
                pattern = self.data[idx % n]
                idx += 1
                if pattern == "<":
                    shifted_rocks = self.shift_rocks_left(rock_set, column)
                if pattern == ">":
                    shifted_rocks = self.shift_rocks_right(rock_set, column)
                rock_set = self.shift_rocks_down(shifted_rocks, column)
                if rock_set == shifted_rocks:
                    column |= shifted_rocks
                    floor_height = max(floor_height, max(
                        y[1] for y in shifted_rocks))
                    break
        return floor_height + 1

    def solve(self) -> None:
        self.sol1 = self.helper(2022)
        self.sol2 = self.helper(1000000000000)

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
