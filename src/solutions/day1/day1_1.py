with open("../../data/day1.txt") as file:
    curr = 0
    res = 0

    for line in file:
        if line == '\n':
            res = max(res, curr)
            curr = 0
            continue
        curr += int(line)

    res = max(res, curr)

    print(res)
