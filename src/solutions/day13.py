import ast


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.two_index = 1
        self.six_index = 2
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day13.txt") as file:
            self.input = file.read().split("\n\n")

# 0 - no decision, 1 - right order, -1 - wrong order
    def comparison(self, left, right) -> int:
        if left == []:
            return 0 if right == [] else 1
        if right == []:
            return -1

        if isinstance(left, int) and isinstance(right, int):
            return -1 if right < left else 0 if right == left else 1
        elif isinstance(left, int):
            return self.comparison([left], right)
        elif isinstance(right, int):
            return self.comparison(left, [right])
        else:
            comparison = self.comparison(left[0], right[0])
            if comparison == 0:
                return self.comparison(left[1:], right[1:])
            return comparison

    def solve(self) -> None:
        for idx, data_item in enumerate(self.input):
            left, right = map(ast.literal_eval, data_item.split("\n"))

            if self.comparison(left, [[2]]) == 1:
                self.two_index += 1
            if self.comparison(right, [[2]]) == 1:
                self.two_index += 1

            if self.comparison(left, [[6]]) == 1:
                self.six_index += 1
            if self.comparison(right, [[6]]) == 1:
                self.six_index += 1

            if self.comparison(left, right) == 1:
                self.sol1 += idx + 1

        self.sol2 = self.six_index * self.two_index

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
