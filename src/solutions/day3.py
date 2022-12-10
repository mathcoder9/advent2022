class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day3.txt") as file:
            self.data = file.read().split("\n")

    def solve1(self) -> None:
        res = 0
        for rucksack in self.data:
            size = len(rucksack)
            overlap = set(rucksack[:size//2]
                          ).intersection(set(rucksack[size//2:]))

            for item in overlap:
                if item.isupper():
                    res += ord(item) + 58 - ord("a") + 1
                else:
                    res += ord(item) - ord("a") + 1

        self.sol1 = res

    def solve2(self) -> None:
        res = 0
        size = len(self.data)
        end = size//3
        for i in range(end):
            overlap = set(self.data[3*i]).intersection(
                set(self.data[3*i+1]).intersection(set(self.data[3*i+2])))

            for item in overlap:
                if item.isupper():
                    res += ord(item) + 58 - ord("a") + 1
                else:
                    res += ord(item) - ord("a") + 1

        self.sol2 = res

    def solve(self) -> None:
        self.solve1()
        self.solve2()

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
