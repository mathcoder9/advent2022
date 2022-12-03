res = 0
with open("../../data/day3.txt") as file:
    data = file.read().split("\n")

    for rucksack in data:
        size = len(rucksack)
        overlap = set(rucksack[:size//2]).intersection(set(rucksack[size//2:]))

        for item in overlap:
            if item.isupper():
                res += ord(item) + 58 - ord("a") + 1
            else:
                res += ord(item) - ord("a") + 1

print(res)
