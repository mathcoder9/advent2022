import time
from collections import deque, defaultdict
from typing import Optional


class Solution:

    def __init__(self) -> None:
        self.sol2 = 0
        self.init_data()
        a = time.time()
        self.sol1 = self.helper(30)
        print("Problem 1 took", time.time() - a, "s")
        a = time.time()
        self.solve_2()
        print("Problem 2 took", time.time() - a, "s")

    def init_data(self) -> None:
        with open("../data/day16.txt") as file:
            data = file.read().split("\n")
        self.adj_list = dict()
        self.flow = dict()
        self.nodes = set()
        for line in data:
            processed_line = line.split(" ")
            node = processed_line[1]
            rate = int(processed_line[4].split("=")[1][:-1])
            self.flow[node] = rate
            if rate > 0:
                self.nodes.add(node)

            self.adj_list[node] = []
            for j in range(9, len(processed_line)):
                neighbour = processed_line[j]
                if neighbour[-1] == ',':
                    self.adj_list[node].append(neighbour[:-1])
                else:
                    self.adj_list[node].append(neighbour)
        self.compress_graph()

    def compress_graph(self) -> None:
        self.compressed_graph = defaultdict(dict)
        for node in {*self.nodes, "AA"}:
            q = deque([(node, 0)])
            seen = set()
            while q:
                curr, dist = q.popleft()
                if curr in seen:
                    continue
                seen.add(curr)

                if curr != node and curr in self.nodes:
                    self.compressed_graph[node][curr] = dist

                for neighbor in self.adj_list[curr]:
                    q.append((neighbor, dist + 1))

    def helper(self, minutes: int, return_paths: Optional[bool] = None) -> object:

        q = deque([("AA", {"AA"}, 0, 0)])  # curr, visited, pressure
        paths = []
        cache = {}
        res = -1
        while q:
            node, visited, time, pressure = q.popleft()
            if time == minutes:
                if return_paths:
                    paths.append((visited, pressure))
                res = max(res, pressure)
                continue

            if cache.get((node, time), -1) >= pressure:
                continue
            cache[(node, time)] = pressure

            added = False
            for item, distance in self.compressed_graph[node].items():
                if item in visited:
                    continue

                if distance + 1 + time > minutes:
                    continue
                added = True
                temp_time_left = minutes-time-distance-1
                q.append((item, {*visited, item}, time + distance + 1,
                         pressure + (temp_time_left * self.flow[item])))

            if not added:
                if return_paths:
                    paths.append((visited, pressure))
                res = max(res, pressure)
                continue

        return res if not return_paths else paths

    def solve_2(self) -> None:
        path_info = sorted(self.helper(26, True), key=lambda x: -x[1])
        n = len(path_info)
        first_path = path_info[0][0]
        limit = n

        # find best disjoint pair of paths - find UB on j by using best path

        for i in range(1, n):
            test_path = path_info[i]
            if len(first_path & test_path[0]) == 1:
                limit = i
                break

        for i in range(n):
            for j in range(i+1, limit+1):
                path_one = path_info[i]
                path_two = path_info[j]
                if len(path_one[0] & path_two[0]) == 1:
                    self.sol2 = max(self.sol2, path_one[1] + path_two[1])

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
