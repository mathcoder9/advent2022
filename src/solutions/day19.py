import time
from math import ceil
from typing import List, Tuple


class Blueprint:
    def __init__(self, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obisidian) -> None:
        self.max_ore = max(int(ore_ore), int(clay_ore), int(obsidian_ore))
        self.max_clay = int(obsidian_clay)
        self.max_obsidian = int(geode_obisidian)
        self.requirements = [(int(ore_ore), 0, 0), (int(clay_ore), 0, 0),
                             (int(obsidian_ore), int(obsidian_clay), 0), (int(geode_ore), 0, int(geode_obisidian))]

    def get_max(self) -> List[int]:
        return [self.max_ore, self.max_clay, self.max_obsidian]

    def build_ore(self, ingredients, machines, type) -> int:
        days = 0
        requirement = self.requirements[type]
        for i in range(3):
            req = requirement[i]
            current = ingredients[i]
            growth_rate = machines[i]
            if req <= current:
                continue
            if growth_rate == 0 and current < req:
                return -1
            else:
                days = max(days, ceil(((req - current)) / growth_rate))
        return days + 1


class Solution:

    triangle_nums = [(i * (i+1)/2) for i in range(32)]

    def __init__(self) -> None:
        self.sol1 = 0
        self.sol2 = 1
        self.init_data()
        self.solve()

    def init_data(self) -> None:
        with open("../data/day19.txt") as file:
            data = file.read().split("\n")
        self.blueprints = []
        for line in data:
            temp = line.split(" ")
            blueprint = Blueprint(
                temp[6], temp[12], temp[18], temp[21], temp[27], temp[30])
            self.blueprints.append(blueprint)

    def solve_blueprint(self, blueprint: Blueprint, total_days: int) -> int:
        stack = [([1, 0, 0, 0], [0, 0, 0, 0], 0)]
        max_geodes = 0
        max_reqs = blueprint.get_max()

        cache_1 = {}
        cache_2 = {}

        def update_stack(machines: List[int], ingredients: List[int], days: int, idx: int) -> None:
            req_days = blueprint.build_ore(ingredients, machines, idx)
            if req_days != -1:

                # check if we can make the machine before day limit
                if req_days + days > total_days:
                    return

                updated_ingredients = [
                    (req_days) * machines[i] + ingredients[i] for i in range(4)]

                for j in range(3):
                    updated_ingredients[j] -= blueprint.requirements[idx][j]

                updated_machines = machines[:]
                updated_machines[idx] += 1
                # check if we can beat max_geode from current state
                if updated_ingredients[3] + (updated_machines[3] * (total_days-days-req_days)) + self.triangle_nums[total_days-days-req_days-1] < max_geodes:
                    return

                # check cache if we have already visited a state
                skip = False
                key = (*updated_machines, *updated_ingredients)
                if key in cache_1:
                    if days + req_days >= cache_1[key]:
                        skip = True
                cache_1[key] = days
                if skip:
                    return

                # check cache if we have already visited a better state
                key = tuple((*updated_machines, days + req_days))
                if key in cache_2:
                    resources = cache_2[key]
                    for resource in resources:
                        if all(resource[i] >= updated_ingredients[i] for i in range(4)):
                            skip = True
                            break
                    if skip:
                        return
                else:
                    cache_2[key] = set()
                cache_2[key].add(tuple(updated_ingredients))

                stack.append(
                    (updated_machines, updated_ingredients, req_days + days))

        while stack:
            machines, ingredients, days = stack.pop()

            max_geodes = max(
                max_geodes, ingredients[3] + (total_days-days) * machines[3])

            # try adding geode
            update_stack(machines, ingredients, days, 3)
            # try adding obisidian
            if machines[2] < max_reqs[2]:
                update_stack(machines, ingredients, days, 2)
            # try adding clay
            if machines[1] < max_reqs[1]:
                update_stack(machines, ingredients, days, 1)
            # try adding ore
            if machines[0] < max_reqs[0]:
                update_stack(machines, ingredients, days, 0)

        return max_geodes

    def solve(self):
        for idx, blueprint in enumerate(self.blueprints):
            self.sol1 += (idx+1) * self.solve_blueprint(blueprint, 24)

        for idx, blueprint in enumerate(self.blueprints):
            if idx > 2:
                break
            self.sol2 *= self.solve_blueprint(blueprint, 32)

    def get_solution(self) -> Tuple[int]:
        return (self.sol1, self.sol2)


a = time.time()
solution = Solution()
print(solution.get_solution())
print("Both parts took", time.time()-a, "s")
