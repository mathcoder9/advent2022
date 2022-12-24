from collections import defaultdict, deque
import time
from typing import Tuple


class Solution:

    operators = {
        "+": lambda a, b: a+b,
        "-": lambda a, b: a-b,
        "*": lambda a, b: a*b,
        "/": lambda a, b: a//b,
    }

    reverse_operators = {
        "-": lambda a, b: a+b,
        "+": lambda a, b: a-b,
        "/": lambda a, b: a*b,
        "*": lambda a, b: a//b,
    }

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day21.txt") as file:
            self.data = file.read().split("\n")

    def init_variables(self, allow_humn: bool) -> None:
        self.number_map = dict()
        self.graph = defaultdict(list)
        self.indegree_map = defaultdict(int)
        self.recipe = dict()
        for line in self.data:
            monkey, info = line.split(":")
            if info[1].isnumeric():
                if not allow_humn and monkey == "humn":
                    continue
                self.number_map[monkey] = int(info[1:])
            else:
                monkey_one = info[1:5]
                operator = info[6]
                monkey_two = info[8:]
                self.graph[monkey_one].append(monkey)
                self.graph[monkey_two].append(monkey)
                self.recipe[monkey] = [monkey_one, monkey_two, operator]
                self.indegree_map[monkey] += 2 if monkey_two != monkey_one else 1

    # topological sort - finds all monkey numbers ~8ms for part 1
    def topological_sort(self, allow_humn: bool) -> None:
        if "root" in self.number_map:
            return self.number_map["root"]

        q = deque()
        for monkey in self.number_map.keys():
            if not allow_humn and monkey == "humn":
                continue
            q.append(monkey)

        processed = set()
        while q:
            monkey = q.popleft()
            if monkey not in self.number_map:
                monkey_one, monkey_two, operator = self.recipe[monkey]
                monkey_val = self.operators[operator](
                    self.number_map[monkey_one], self.number_map[monkey_two])
                self.number_map[monkey] = monkey_val

            processed.add(monkey)
            for neighbour in self.graph[monkey]:
                if neighbour in processed:
                    continue
                self.indegree_map[neighbour] -= 1
                if self.indegree_map[neighbour] == 0:
                    q.append(neighbour)

    # work backwards ~8ms for part 2

    def helper(self) -> int:

        monkey_one, monkey_two, _ = self.recipe["root"]

        if monkey_two in self.number_map:
            monkey_one, monkey_two = monkey_two, monkey_one

        res = self.number_map[monkey_one]
        monkey = monkey_two

        while monkey != "humn":

            monkey_one, monkey_two, operator = self.recipe[monkey]

            # if we know monkey_two value
            if monkey_two in self.number_map:
                if operator == "+":
                    res = self.reverse_operators[operator](
                        res, self.number_map[monkey_two])
                elif operator == "-":
                    res = self.reverse_operators[operator](
                        self.number_map[monkey_two], res)
                elif operator == "*":
                    res = self.reverse_operators[operator](
                        res, self.number_map[monkey_two])
                elif operator == "/":
                    res = self.reverse_operators[operator](
                        self.number_map[monkey_two], res)
                monkey = monkey_one
                continue

            # if we know monkey_one value
            if operator == "+":
                res = self.reverse_operators[operator](
                    res, self.number_map[monkey_one])
            elif operator == "-":
                res = self.operators[operator](
                    self.number_map[monkey_one], res)
            elif operator == "*":
                res = self.reverse_operators[operator](
                    res, self.number_map[monkey_one])
            elif operator == "/":
                res = self.operators[operator](
                    self.number_map[monkey_one], res)
            monkey = monkey_two

        return res

    def solve(self) -> None:
        # solve 1
        self.init_variables(True)
        self.topological_sort(True)
        self.sol1 = self.number_map["root"]
        self.init_variables(False)
        self.topological_sort(False)
        self.sol2 = self.helper()

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
