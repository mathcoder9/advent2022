class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day2.txt") as file:
            self.data = file.read().split("\n")

    def solve1(self) -> None:
        score = 0
        for line in self.data:
            moves = line.split(" ")
            oppMove = ord(moves[0])-ord('A')
            myMove = ord(moves[1][0])-ord('X')
            score += myMove + 1

            if oppMove == myMove:
                score += 3
                continue

            if (myMove + 2) % 3 == oppMove:
                score += 6

        self.sol1 = score

    def solve2(self) -> None:
        score = 0
        for line in self.data:
            moves = line.split(" ")
            oppMove = ord(moves[0])-ord('A')
            outcome = ord(moves[1][0])-ord('X')
            score += outcome * 3

            if outcome == 0:
                myMove = (oppMove + 2) % 3
                score += myMove + 1
            elif outcome == 1:
                score += oppMove + 1
            else:
                myMove = (oppMove + 1) % 3
                score += myMove + 1

        self.sol2 = score

    def solve(self) -> None:
        self.solve1()
        self.solve2()

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
