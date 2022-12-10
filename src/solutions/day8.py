class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve1()
        self.solve2()

    def init_data(self) -> None:
        with open("../data/day8.txt") as file:
            self.data = [list(map(int, line))
                         for line in file.read().split("\n")]

    def solve1(self) -> None:
        seen = set()
        m = len(self.data)
        n = len(self.data[0])

        for i in range(m):
            biggest = -1
            for j in range(n):
                curr = self.data[i][j]
                if curr > biggest:
                    if (i, j) not in seen:
                        seen.add((i, j))
                        self.sol1 += 1
                    biggest = curr

            biggest = -1
            for j in range(n-1, -1, -1):
                curr = self.data[i][j]
                if curr > biggest:
                    if (i, j) not in seen:
                        seen.add((i, j))
                        self.sol1 += 1
                    biggest = curr

        for j in range(n):
            biggest = -1
            for i in range(m):
                curr = self.data[i][j]
                if curr > biggest:
                    if (i, j) not in seen:
                        seen.add((i, j))
                        self.sol1 += 1
                    biggest = curr

            biggest = -1
            for i in range(m-1, -1, -1):
                curr = self.data[i][j]
                if curr > biggest:
                    if (i, j) not in seen:
                        seen.add((i, j))
                        self.sol1 += 1
                    biggest = curr

    def solve2(self) -> None:
        m = len(self.data)
        n = len(self.data[0])

        cover = [[1]*n for _ in range(m)]

        for i in range(1, m-1):
            for j in range(1, n-1):
                height = self.data[i][j]

                left_count = 0
                for a in range(j-1, -1, -1):
                    left_count += 1
                    if self.data[i][a] >= height:
                        break
                cover[i][j] *= left_count

                right_count = 0
                for a in range(j+1, n):
                    right_count += 1
                    if self.data[i][a] >= height:
                        break
                cover[i][j] *= right_count

        for j in range(1, n-1):
            for i in range(1, m-1):
                height = self.data[i][j]

                up_count = 0
                for a in range(i-1, -1, -1):
                    up_count += 1
                    if self.data[a][j] >= height:
                        break
                cover[i][j] *= up_count

                down_count = 0
                for a in range(i+1, m):
                    down_count += 1
                    if self.data[a][j] >= height:
                        break
                cover[i][j] *= down_count

                self.sol2 = max(self.sol2, cover[i][j])

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
