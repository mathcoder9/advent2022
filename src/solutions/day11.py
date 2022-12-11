from collections import deque


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        self.monkey_items = [deque([63, 57]), deque([82, 66, 87, 78, 77, 92, 83]), deque([97, 53, 53, 85, 58, 54]), deque([50]), deque([
            64, 69, 52, 65, 73]), deque([57, 91, 65]), deque([67, 91, 84, 78, 60, 69, 99, 83]), deque([58, 78, 69, 65])]

        self.monkey_operation = [lambda x: x*11, lambda x: x+1, lambda x: x*7,
                                 lambda x: x+3, lambda x: x+6, lambda x: x+5, lambda x: x**2, lambda x: x+7]

        self.monkey_test = [7, 11, 13, 3, 17, 2, 5, 19]

        self.monkey_catch = [[6, 2], [5, 0], [4, 3],
                             [1, 7], [3, 7], [0, 6], [2, 4], [5, 1]]

    def helper(self, rounds, worry_divisor) -> int:
        count = [0 for _ in range(8)]

        for _ in range(rounds):
            for monkey_number in range(8):
                divisibility_num = self.monkey_test[monkey_number]
                item_count = len(self.monkey_items[monkey_number])
                count[monkey_number] += item_count
                for _ in range(item_count):
                    worry = self.monkey_items[monkey_number].popleft(
                    )
                    new_worry = (self.monkey_operation[monkey_number](
                        worry) // worry_divisor) % 9699690  # lcm of monkeys_test
                    passed_test = 0 if new_worry % divisibility_num == 0 else 1
                    next_monkey = self.monkey_catch[monkey_number][passed_test]
                    self.monkey_items[next_monkey].append(new_worry)

        highest = -1
        second_highest = -2

        for inspects in count:
            if inspects > highest:
                second_highest = highest
                highest = inspects
            elif inspects > second_highest:
                second_highest = inspects
        return (highest * second_highest)

    def solve(self) -> None:
        self.init_data()
        self.sol1 = self.helper(20, 3)
        self.init_data()
        self.sol2 = self.helper(10000, 1)

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
