import copy
import math


def findPathOrder(graph, start, depth):             # while it is possible to increase the score by reaching another
    unvisited = set()                               # tile, find the next best tile to go to and set it as visited
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


def findBestScore(graph, start, unvisited, depth, inRecurse=False):     # find the best permutation of depth d where
    if depth == 0:                                                      # the sum of path scores is highest and
        return 0, [start]                                               # return the first node in the permutation
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
        return maxscore, path
    # print(path)
    return bestStart




