import heapq


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../../data/day1.txt") as file:
            self.data = file.read().split("\n")

    def solve1(self) -> None:
        curr = 0
        res = 0
        for line in self.data:
            if line == '':
                res = max(res, curr)
                curr = 0
                continue
            curr += int(line)

        res = max(res, curr)
        self.sol1 = res

    def solve2(self) -> None:
        curr = 0
        heap = []

        for line in self.data:
            if line == '':
                heapq.heappush(heap, -curr)
                curr = 0
                continue
            curr += int(line)

        heapq.heappush(heap, -curr)

        self.sol2 = -(heapq.heappop(heap) +
                      heapq.heappop(heap) + heapq.heappop(heap))

    def solve(self) -> None:
        self.solve1()
        self.solve2()

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
