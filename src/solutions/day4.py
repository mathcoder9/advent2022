from typing import List


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day4.txt") as file:
            self.data = file.read().split("\n")

    def convert_data(self, intervalData) -> List[List[int]]:
        intervals = intervalData.split(",")
        pairs = []
        for interval in intervals:
            temp = interval.split("-")
            pairs.append([int(temp[0]), int(temp[1])])

        return pairs

    def check_overlap(self, pairs) -> bool:
        pair1, pair2 = pairs
        return not min(pair1[1], pair2[1]) < max(pair1[0], pair2[0])

    def check_contains(self, pairs) -> bool:
        pair1, pair2 = pairs
        if pair1[0] == pair2[0]:
            return True
        elif pair1[0] < pair2[0]:
            return pair2[1] <= pair1[1]
        else:
            return pair1[1] <= pair2[1]

    def solve(self) -> None:
        for item in self.data:
            pairs = self.convert_data(item)
            if self.check_contains(pairs):
                self.sol1 += 1
            if self.check_overlap(pairs):
                self.sol2 += 1

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
