import heapq

with open("../../data/day1.txt") as file:

    curr = 0
    heap = []

    for line in file:
        if line == '\n':
            heapq.heappush(heap, -curr)
            curr = 0
            continue
        curr += int(line)

    heapq.heappush(heap, -curr)

    print(-(heapq.heappop(heap) + heapq.heappop(heap) + heapq.heappop(heap)))
