import copy
import math


def findPathOrder(graph, start, depth):
    unvisited = set()
    path = [start]
    for g in graph:
        if g == start:
            continue
        unvisited.add(g)
    currentPos = start
    while len(unvisited) > 0:
        nextPos = findBestScore(graph, currentPos, unvisited, depth)
        if nextPos is None:
            break
        path.append(nextPos)
        unvisited.remove(nextPos)
        currentPos = nextPos
    return path


def findBestScore(graph, start, unvisited, depth, inRecurse=False):

    if depth == 0:
        return (0, [start])
    path = [start]
    maxscore = 0
    bestStart = None
    bestPath = []
    for u in unvisited:
        if u == start:
            continue
        score = graph[start][u]["SCORE"]
        uCpy = copy.deepcopy(unvisited)
        uCpy.remove(u)
        nextBest = findBestScore(graph, u, uCpy, depth-1, True)
        score += nextBest[0]
        if score > maxscore:
            maxscore = score
            bestStart = u
            bestPath = nextBest[1]

    path.append(bestPath)
    if inRecurse:
        return (maxscore, path)
    # print(path)
    return bestStart




