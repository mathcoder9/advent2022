from __future__ import annotations
import time
from typing import Tuple


class Node:

    def __init__(self, val: int = 0, next: Node = None, prev: Node = None) -> None:
        self.val = val
        self.next = next
        self.prev = prev


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day20.txt") as file:
            self.data = file.read().split("\n")

    def init_dll(self) -> None:

        start = Node(int(self.data[0]))
        self.nodes = [start]

        for idx, num in enumerate(self.data):
            if idx == 0:
                continue
            value = int(num)
            node = Node(value)
            if value == 0:
                self.start = node
            start.next = node
            node.prev = start
            self.nodes.append(node)
            start = start.next

        start.next = self.nodes[0]
        self.nodes[0].prev = start

    def helper(self, rounds: int, multiplier: int) -> int:
        size = len(self.nodes)
        reduced_multiplier = multiplier % (size - 1)
        for _ in range(rounds):
            for node in self.nodes:
                moves = (node.val * reduced_multiplier) % (
                    size - 1) if node.val >= 0 else ((size - 1) - ((- node.val * reduced_multiplier) % (size - 1)))

                if moves == 0:
                    continue

                prev = node.prev
                next = node.next
                prev.next = next
                next.prev = prev

                new_start = node
                for _ in range(moves):
                    new_start = new_start.next

                temp = new_start.next
                new_start.next = node
                node.next = temp
                temp.prev = node
                node.prev = new_start

        zero = self.start
        res = 0

        for j in range(3000):
            zero = zero.next
            if (j+1) % 1000 == 0:
                res += zero.val * multiplier

        return res

    def solve(self) -> None:
        self.init_dll()
        self.sol1 = self.helper(1, 1)
        self.init_dll()
        self.sol2 = self.helper(10, 811589153)

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
