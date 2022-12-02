score = 0
with open("../../data/day2.txt") as file:
    for line in file:
        moves = line.split(" ")
        oppMove = ord(moves[0])-ord('A')
        outcome = ord(moves[1][0])-ord('X')
        score += outcome * 3

        if outcome == 0:
            myMove = (oppMove + 2) % 3
            score += myMove + 1
        elif outcome == 1:
            score += oppMove + 1
        else:
            myMove = (oppMove + 1) % 3
            score += myMove + 1

print(score)
