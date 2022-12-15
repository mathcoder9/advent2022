import time
from typing import List
# 5.5ms for both parts


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day15.txt") as file:
            data = file.read().split("\n")
        self.balls = []
        for line in data:
            processed = line.split("=")
            sensor = (int(processed[1][:processed[1].index(",")]), int(
                processed[2][:processed[2].index(":")]))
            beacon = (
                int(processed[3][:processed[3].index(",")]), int(processed[4]))

            self.balls.append([sensor, beacon, self.distance(sensor, beacon)])

    def distance(self, a: List[int], b: List[int]) -> int:
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def calculate_range(self, list_of_intervals: List[List[int]]) -> int:
        res = 0
        if len(list_of_intervals) == 0:
            return res

        prev_interval = None
        for start, end in sorted(list_of_intervals):
            if not prev_interval:
                prev_interval = [start, end]
            elif prev_interval[1] >= start - 1:
                prev_interval[1] = max(prev_interval[1], end)
            else:
                res += prev_interval[1] - prev_interval[0]
                prev_interval = [start, end]

        res += prev_interval[1] - prev_interval[0]
        return res

    def solve_1(self) -> None:
        excluded = list()
        found = set()

        for item in self.balls:
            center, beacon, radius = item
            center_x, center_y = center
            beacon_x, beacon_y = beacon
            y_dist = abs(center_y - 2000000)
            if beacon_y == 2000000:
                found.add(beacon_x)

            if y_dist <= radius:
                excluded.append([center_x - radius + y_dist,
                                center_x + radius - y_dist])

        self.sol1 = self.calculate_range(excluded)
        self.sol1 -= len(found)

    def check_point(self, point: List[int]) -> bool:
        for item in self.balls:
            center, _, radius = item
            if self.distance(center, point) <= radius:
                return False
        return True

    def solve_2(self) -> None:
        b = time.time()
        pos_diags = set()  # diagonals are parameterised by y intercept
        neg_diags = set()

        for item in self.balls:
            center, _, radius = item

            center_x, center_y = center
            pos_diags.add(center_y-radius-center_x - 1)
            pos_diags.add(center_y+radius-center_x + 1)
            neg_diags.add(center_y-radius+center_x - 1)
            neg_diags.add(center_y+radius+center_x + 1)
        # get intersections
        for pos in pos_diags:
            for neg in neg_diags:

                y_intercept = (pos + neg)/2
                x_intercept = (neg - pos)/2

                if x_intercept.is_integer() and y_intercept.is_integer() and 0 <= x_intercept <= 4000000 and 0 <= y_intercept <= 4000000:
                    point = [x_intercept, y_intercept]
                    if self.check_point(point):
                        self.sol2 = int(x_intercept * 4000000 + y_intercept)
                        return

    def solve(self) -> None:
        self.solve_1()
        self.solve_2()

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
