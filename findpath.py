import copy
import math
from copy import deepcopy

def findPath(board, sourceX, sourceY):
    matrix = []
    paths = []
    goals = {}
    for y in range(board.height):
        row = []
        pathrow = []
        for x in range(board.width):
            row.append(math.inf)
            pathrow.append([])
        matrix.append(row)
        paths.append(pathrow)
    matrix[sourceY][sourceX] = 0
    bests = {(sourceX, sourceY): 0}
    paths[sourceY][sourceX] = [(sourceX, sourceY)]
    current = [(sourceX, sourceY)]

    while len(current) > 0:
        next = []
        for tilePos in current:
            tile = board.matrix[tilePos[1]][tilePos[0]]
            for n in tile.neighbors:
                neighbor = n[0]
                currentWeight = matrix[neighbor.y][neighbor.x]
                newWeight = matrix[tile.y][tile.x] + n[1]
                if newWeight < currentWeight:
                    next.append((neighbor.x, neighbor.y))
                    matrix[neighbor.y][neighbor.x] = newWeight
                    paths[neighbor.y][neighbor.x] = copy.deepcopy(paths[tile.y][tile.x])
                    paths[neighbor.y][neighbor.x].append((neighbor.x, neighbor.y))
                    if neighbor.status == "TARGET":
                        goals[(neighbor.x, neighbor.y)] = (newWeight, paths[neighbor.y][neighbor.x])


        current = next
    print(f"STARTING AT {sourceX}, {sourceY}")
    for g in goals:
        print(f"PATH TO {g} (weight {goals[g][0]}): {goals[g][1]}")

