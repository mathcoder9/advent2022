from __future__ import annotations
from bisect import bisect_right


class TreeNode:
    def __init__(self, name: str, parent: TreeNode = None) -> None:
        self.parent = parent
        self.name = name
        self.children = dict()
        self.size = 0
        self.files = set()

    def add_dir(self, name: str) -> None:
        if name not in self.children:
            self.children[name] = TreeNode(name, self)

    def get_child(self, name: str) -> TreeNode:
        return self.children[name]

    def add_file(self, file_name: str, file_size: str) -> None:
        if file_name not in self.files:
            self.files.add(file_name)
            self.size += int(file_size)

    def get_parent(self) -> TreeNode:
        return self.parent

    def get_size(self) -> int:
        return self.size

# The idea is to create a tree data structure with nodes being directories. Each node has a 'size' which is the sum of the file sizes of all files (not including files in subdirectories) of a directory. Then, recursively compute the total file size of each directory (including files in subdirectories) of the tree and add to the sol1 if it exceeds the maximum file size. We also store the file size of each directory and use a binary search for solution 2 (alternatively we could run helper()) again and keep track of the smallest directory size exceeding the required space we need to delete as we go).
# Tree initialisation - O(n) space O(n) time where n is num of commands given
# Solution 1 - O(n) time O(1) extra space
# Solution 2 - O(nlogn) time O(d) extra space where d is num of directories. Can be improved to O(n) time O(1) extra space if we run helper() again.


class Solution:

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.directory_sizes = []
        self.init_data()
        self.init_tree()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day7.txt") as file:
            self.data = file.read().split("\n")

    def init_tree(self) -> None:
        self.root = TreeNode('/')
        current_node = self.root
        for idx, line in enumerate(self.data):
            if idx == 0:
                continue

            # file size case
            if line[0].isnumeric():
                file_size, file_name = line.split(" ")
                current_node.add_file(file_name, file_size)
                continue

            # new dir case
            if line[0] == 'd':
                subdirectory = line.split(" ")[1]
                current_node.add_dir(subdirectory)
                continue

            # skip $ ls case
            if line[2] == "l":
                continue

            path = line.split()[2]
            if path == '..':
                current_node = current_node.get_parent()
            else:
                current_node = current_node.get_child(path)

    def helper(self, root: TreeNode) -> int:
        if not root:
            return 0

        size = root.get_size()
        for subdirectory in root.children.values():
            size += self.helper(subdirectory)

        self.directory_sizes.append(size)
        if size <= 100000:
            self.sol1 += size

        return size

    def solve(self) -> None:
        root_directory_size = self.helper(self.root)
        space_required = root_directory_size - 40000000
        self.directory_sizes.sort()

        self.sol2 = self.directory_sizes[bisect_right(
            self.directory_sizes, space_required)]

    def get_solution(self) -> tuple:
        return (self.sol1, self.sol2)


solution = Solution()
print(solution.get_solution())
