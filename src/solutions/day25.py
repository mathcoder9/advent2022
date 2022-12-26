import time
from typing import Tuple


class Solution:

    snafu_int_conv = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

    int_snafu_conv = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve_1()

    def init_data(self) -> None:
        with open("../data/day25.txt") as file:
            self.data = file.read().split("\n")

    def convert_SNAFU_int(self, snafu: str) -> int:
        num = 0
        for letter in snafu:
            num *= 5
            num += self.snafu_int_conv[letter]
        return num

    def convert_int_SNAFU(self, num: int) -> str:
        snafu = ""
        while num != 0:
            unit = (num + 2) % 5 - 2
            snafu += self.int_snafu_conv[unit]
            num = (num - unit) // 5
        return snafu[::-1]

    def solve_1(self) -> None:
        total = 0
        for data in self.data:
            total += self.convert_SNAFU_int(data)
        self.sol1 = self.convert_int_SNAFU(total)

    def get_solution(self) -> Tuple[int]:
        return (self.sol1)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Took", time.time()-a, "s")
