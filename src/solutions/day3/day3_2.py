res = 0
with open("../../data/day3.txt") as file:
    data = file.read().split("\n")

    size = len(data)
    end = size//3
    for i in range(end):
        overlap = set(data[3*i]).intersection(
            set(data[3*i+1]).intersection(set(data[3*i+2])))

        for item in overlap:
            if item.isupper():
                res += ord(item) + 58 - ord("a") + 1
            else:
                res += ord(item) - ord("a") + 1

print(res)
