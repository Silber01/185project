import copy
import math


def findPaths(board, sourceX, sourceY):
    matrix = []
    paths = []
    goals = {}
    checks = 0
    for y in range(board.height):                               # converts matrix into graph with unknown distances from
        row = []                                                # source (set to infinity)
        pathrow = []
        for x in range(board.width):
            row.append(math.inf)
            pathrow.append([])
        matrix.append(row)
        paths.append(pathrow)
    matrix[sourceY][sourceX] = 0
    paths[sourceY][sourceX] = [(sourceX, sourceY)]
    current = [(sourceX, sourceY)]

    while len(current) > 0:                                     # implements bfs pathfinding and saves tiles to
        nextTiles = []                                          # traverse for best path from the given tile to each
        for tilePos in current:                                 # other tile
            tile = board.matrix[tilePos[1]][tilePos[0]]
            for n in tile.neighbors:
                neighbor = n[0]
                currentWeight = matrix[neighbor.y][neighbor.x]
                newWeight = matrix[tile.y][tile.x] + n[1]
                checks += 1
                if newWeight < currentWeight:
                    nextTiles.append((neighbor.x, neighbor.y))
                    matrix[neighbor.y][neighbor.x] = newWeight
                    paths[neighbor.y][neighbor.x] = copy.deepcopy(paths[tile.y][tile.x])
                    paths[neighbor.y][neighbor.x].append([neighbor.x, neighbor.y])
                    if neighbor.status == "TARGET":
                        goals[(neighbor.x, neighbor.y)] = {"SCORE": neighbor.score - newWeight, "PATH": paths[neighbor.y][neighbor.x]}
        current = nextTiles
    # print(goals)
    # print(f"STARTING AT {sourceX}, {sourceY}")
    # for g in goals:
    #     weight = goals[g]["WEIGHT"]
    #     path = goals[g]["PATH"]
    #     print(f"PATH TO {g} (weight {weight}): {path}")
    # print(f"DONE IN {checks} CHECKS")
    return goals


def makeGraph(board, targets):                                  # for all targets, find all paths from it to all other
    graph = {}                                                  # tiles, essentially creating a more condensed graph
    for t in targets:
        goals = findPaths(board, t[0], t[1])
        graph[(t[0], t[1])] = goals
    return graph


def getTargets(board, targetsDir, startDir):                # converts targets.txt into a set of coordinates
    targets = []
    targetList = open(targetsDir, "r").read().split("\n")
    start = open(startDir, "r").read().split("\n")
    targetList.append(start[0])
    for t in targetList:
        tData = t.split(",")
        if len(tData) > 3 or len(tData) < 2:
            print(f"{tData} is not a valid target!")
            continue
        try:
            x = int(tData[0])
            y = int(tData[1])
        except ValueError:
            print(f"{tData} is not a valid target!")
            continue
        if x < 0 or x >= board.width or y < 0 or y >= board.height:
            print(f"{tData} is out of range!")
            continue
        targets.append((x, y))
    return targets




