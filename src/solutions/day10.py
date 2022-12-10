class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day10.txt") as file:
            self.data = [line.split(" ")
                         for line in file.read().split("\n")]

    def helper(self) -> None:
        strength = 0
        cycle = 0
        value = 1

        self.screen = [['.']*40 for _ in range(6)]

        stack = [220, 180, 140, 100, 60, 20]
        valueToAdd = 0
        for line in self.data:
            value += valueToAdd

            if line[0] == 'noop':
                self.update_screen(cycle, value)
                cycle += 1
                valueToAdd = 0
            else:
                self.update_screen(cycle, value)
                self.update_screen(cycle+1, value)
                cycle += 2
                valueToAdd = int(line[1])

            if stack and stack[-1] <= cycle:
                strength += stack.pop() * value

        if stack and stack[-1] == cycle:
            value += valueToAdd
            strength += stack.pop() * value

        self.sol1 = strength

    def update_screen(self, cycle, value) -> None:
        if abs(cycle % 40-value) <= 1:
            self.screen[cycle // 40][cycle % 40] = '#'

    def solve(self) -> None:
        self.helper()

    def get_solution(self) -> tuple:
        return (self.sol1)

    def print_screen(self) -> None:
        for i in range(6):
            print(self.screen[i])


solution = Solution()
print(solution.get_solution())
solution.print_screen()
