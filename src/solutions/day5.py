from collections import deque
from copy import deepcopy


class Solution:

    def __init__(self) -> None:
        self.sol1 = []
        self.sol2 = []
        self.init_data()
        self.solve1()
        self.solve2()

    def init_data(self) -> None:
        with open("../data/day5.txt") as file:
            data = file.read().split("\n")

        size = len(data)
        idx = data.index('')
        length = len(data[0])
        self.deques = [deque() for _ in range(length//4+1)]

        for i in range(0, idx-1):
            for j in range(length//4 + 1):
                if data[i][4*j+1] == ' ':
                    continue
                self.deques[j].appendleft(data[i][4*j+1])

        self.commands = []

        for i in range(idx+1, size):
            splitData = data[i].split(" ")
            self.commands.append(
                [int(splitData[1]), int(splitData[3]), int(splitData[5])])

    def solve1(self) -> None:
        dequeList = deepcopy(self.deques)
        for moves, startPile, endPile in self.commands:
            for _ in range(moves):
                dequeList[endPile-1].append(dequeList[startPile-1].pop())

        for item in dequeList:
            self.sol1.append(item[-1])

    def solve2(self) -> None:
        dequeList = self.deques
        for moves, startPile, endPile in self.commands:
            temp = deque()
            for _ in range(moves):
                temp.appendleft(dequeList[startPile-1].pop())

            for letter in temp:
                dequeList[endPile-1].append(letter)

        for item in dequeList:
            self.sol2.append(item[-1])

    def get_solution(self) -> tuple:
        return ("".join(self.sol1), "".join(self.sol2))


solution = Solution()
print(solution.get_solution())
