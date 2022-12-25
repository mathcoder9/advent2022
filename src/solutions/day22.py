from bisect import bisect_left
import time
from typing import Tuple


class Solution:

    jumps = {
        (1, 2): (0, lambda i, j: (149 - i, 0)),
        (1, 3): (0, lambda i, j: (j+100, 0)),
        (2, 0): (2, lambda i, j: (149-i, 99)),
        (2, 1): (2, lambda i, j: (j-50, 99)),
        (2, 3): (3, lambda i, j: (199, j-100)),
        (3, 0): (3, lambda i, j: (49, i+50)),
        (3, 2): (1, lambda i, j: (100, i-50)),
        (4, 0): (2, lambda i, j: (149-i, 149)),
        (4, 1): (2, lambda i, j: (100+j, 49)),
        (5, 2): (0, lambda i, j: (149-i, 50)),
        (5, 3): (0, lambda i, j: (50+j, 50)),
        (6, 0): (3, lambda i, j: (149, i-100)),
        (6, 1): (1, lambda i, j: (0, j+100)),
        (6, 2): (1, lambda i, j: (0, i-100)),
    }

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 0
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day22.txt") as file:
            diagram, self.commands = file.read().split("\n\n")
        diagram_lines = diagram.split("\n")
        length = max(len(line) for line in diagram_lines)
        self.col_walls = [[] for _ in range(length)]
        self.row_walls = []
        self.col_range = [[-1, -1] for _ in range(length)]
        self.row_range = []
        self.walls = set()
        for row, line in enumerate(diagram_lines):
            walls = []
            start_row = -1
            end_row = 0
            for col, char in enumerate(line):
                if char == " ":
                    continue

                if self.col_range[col][0] == -1:
                    self.col_range[col][0] = row

                self.col_range[col][1] = row

                if start_row == -1:
                    start_row = col

                end_row = col
                if char == "#":
                    self.walls.add((row, col))
                    walls.append(col)
                    self.col_walls[col].append(row)
            self.row_walls.append(walls)
            self.row_range.append([start_row, end_row])

    #todo: clean
    def move(self, position, steps, direction):
        if steps == 0:
            return position

        row, column = position

        row_length = self.row_range[row][1] - \
            self.row_range[row][0] + 1

        col_length = self.col_range[column][1] - \
            self.col_range[column][0] + 1

        if direction == 0:
            if len(self.row_walls[row]) == 0:
                return (row, (column - self.row_range[row][0] + steps) % row_length + self.row_range[row][0])

            idx = bisect_left(self.row_walls[row], column)
            dist_to_wall = (self.row_walls[row][0] - self.row_range[row][0]) + (self.row_range[row][1] - column) + 1 if idx == len(
                self.row_walls[row]) else self.row_walls[row][idx] - column

            return (row, (column - self.row_range[row][0] + min(steps, dist_to_wall - 1)) % row_length + self.row_range[row][0])
        elif direction == 2:
            if len(self.row_walls[row]) == 0:
                return (row, (column - self.row_range[row][0] - steps) % row_length + self.row_range[row][0])

            idx = bisect_left(self.row_walls[row], column)

            dist_to_wall = (self.row_range[row][1] - self.row_walls[row][-1]) + (
                column - self.row_range[row][0]) + 1 if idx == 0 else column - self.row_walls[row][idx-1]
            return (row, (column - self.row_range[row][0] - min(steps, dist_to_wall - 1)) % row_length + self.row_range[row][0])
        elif direction == 1:
            if len(self.col_walls[column]) == 0:
                return ((row - self.col_range[column][0] + steps) % col_length + self.col_range[column][0], column)

            idx = bisect_left(self.col_walls[column], row)
            dist_to_wall = (self.col_walls[column][0] - self.col_range[column][0]) + (self.col_range[column][1] - row) + 1 if idx == len(
                self.col_walls[column]) else self.col_walls[column][idx] - row
            return ((row - self.col_range[column][0] + min(steps, dist_to_wall - 1)) % col_length + self.col_range[column][0], column)
        else:
            if len(self.col_walls[column]) == 0:
                return ((row - self.col_range[column][0] - steps) % col_length + self.col_range[column][0], column)

            idx = bisect_left(self.col_walls[column], row)
            dist_to_wall = (self.col_range[column][1] - self.col_walls[column][-1]) + (
                row - self.col_range[column][0]) + 1 if idx == 0 else row - self.col_walls[column][idx-1]

            return ((row - self.col_range[column][0] - min(steps, dist_to_wall - 1)) % col_length + self.col_range[column][0], column)

    def helper(self):

        position = (0, self.row_range[0][0])
        direction = 0

        steps = 0
        for char in self.commands:
            if char.isnumeric():
                steps *= 10
                steps += int(char)
                continue

            position = self.move(position, steps, direction)
            steps = 0

            if char == "L":
                direction -= 1
            else:
                direction += 1
            direction %= 4

        if steps != 0:
            position = self.move(position, steps, direction)

        return 1000*(position[0]+1) + 4*(position[1]+1) + direction

    # cube faces are numbered:          1 2
    #                                   3
    #                                 5 4
    #                                 6
    def get_cube_face(self, position):
        row, col = position
        row_idx = row // 50
        col_idx = col // 50
        if row_idx == 0:
            return col_idx
        elif row_idx == 1:
            return 3
        elif row_idx == 2:
            return 5 if col_idx == 0 else 4
        else:
            return 6

    def next_position(self, position, direction):
        row, col = position
        row_range = self.row_range[row]
        col_range = self.col_range[col]

        if direction == 0 and col + 1 <= row_range[1]:
            return ((row, col + 1), direction)
        if direction == 2 and col - 1 >= row_range[0]:
            return ((row, col - 1), direction)
        if direction == 1 and row + 1 <= col_range[1]:
            return ((row + 1, col), direction)
        if direction == 3 and row - 1 >= col_range[0]:
            return ((row - 1, col), direction)

        new_direction, lambda_fun = self.jumps[self.get_cube_face(
            position), direction]
        return (lambda_fun(row, col), new_direction)

    def move_2(self, position, steps, direction):

        for _ in range(steps):
            next_position, next_direction = self.next_position(
                position, direction)
            if next_position in self.walls:
                break
            position, direction = next_position, next_direction

        return (position, direction)

    def helper_2(self):
        position = (0, self.row_range[0][0])
        direction = 0

        steps = 0
        for char in self.commands:
            if char.isnumeric():
                steps *= 10
                steps += int(char)
                continue

            position, direction = self.move_2(position, steps, direction)
            steps = 0

            if char == "L":
                direction -= 1
            else:
                direction += 1
            direction %= 4

        if steps != 0:
            position = self.move(position, steps, direction)

        return 1000*(position[0]+1) + 4*(position[1]+1) + direction

    def solve(self):
        a = time.time()
        self.sol1 = self.helper()
        print("Part 1 took", time.time()-a, "s")  # ~6ms
        b = time.time()
        self.sol2 = self.helper_2()
        print("Part 2 took", time.time()-b, "s")  # ~15ms

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
