class Solution:

    def __init__(self) -> None:
        self.sol1 = -1
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day14.txt") as file:
            self.data = file.read().split("\n")
        self.rocks = set()
        self.lowest_level = -1
        for line in self.data:
            arr = [list(map(int, coordinate.split(",")))
                   for coordinate in line.split(" -> ")]

            for i in range(len(arr)-1):
                pointA = arr[i]
                pointB = arr[i+1]
                self.lowest_level = max(
                    self.lowest_level, pointA[1], pointB[1])
                if pointA[0] == pointB[0]:
                    for j in range(min(pointA[1], pointB[1]), max(pointA[1], pointB[1]) + 1):
                        self.rocks.add((pointA[0], j))
                else:
                    for j in range(min(pointA[0], pointB[0]), max(pointA[0], pointB[0]) + 1):
                        self.rocks.add((j, pointA[1]))

    def solve(self) -> None:
        count_sol1 = True
        while True:
            x = 500
            y = 0
            if (x, y) in self.rocks:
                break
            if count_sol1:
                self.sol1 += 1
            self.sol2 += 1
            while True:
                if y < self.lowest_level + 1:
                    if (x, y+1) not in self.rocks:
                        y += 1
                        continue
                    elif (x-1, y+1) not in self.rocks:
                        x -= 1
                        y += 1
                        continue
                    elif (x+1, y+1) not in self.rocks:
                        x += 1
                        y += 1
                        continue
                self.rocks.add((x, y))
                break
            if y > self.lowest_level:
                count_sol1 = False

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
