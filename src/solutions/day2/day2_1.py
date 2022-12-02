score = 0
with open("../../data/day2.txt") as file:
    for line in file:
        moves = line.split(" ")
        oppMove = ord(moves[0])-ord('A')
        myMove = ord(moves[1][0])-ord('X')
        score += myMove + 1

        if oppMove == myMove:
            score += 3
            continue

        if (myMove + 2) % 3 == oppMove:
            score += 6

print(score)
