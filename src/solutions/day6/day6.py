class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../../data/day6.txt") as file:
            self.data = file.read()

    def addToStore(self, data, store, store_size) -> list:
        if data in store:
            store[data] += 1
        else:
            store[data] = 1
            store_size += 1

        return [store, store_size]

    def removeFromStore(self, data, store, store_size) -> list:
        if store[data] == 1:
            del store[data]
            store_size -= 1
        else:
            store[data] -= 1

        return [store, store_size]

    def helper(self, num_of_markers) -> None:
        data = self.data
        size = len(data)
        start = num_of_markers
        store = dict()
        store_size = 0

        for i in range(start):
            store, store_size = self.addToStore(data[i], store, store_size)

        if store_size == num_of_markers:
            return start + 1

        for i in range(num_of_markers, size):

            store, store_size = self.removeFromStore(
                data[i-num_of_markers], store, store_size)
            store, store_size = self.addToStore(data[i], store, store_size)

            if store_size == num_of_markers:
                return i + 1

    def solve(self) -> None:
        self.sol1 = self.helper(4)
        self.sol2 = self.helper(14)

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
