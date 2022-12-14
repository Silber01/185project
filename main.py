import os
import random
import json
import pygame
from boardData import *
from findPath import *
from findPathOrder import *
import time


with open("setup.json", "r") as readFile:                                   # implements setup.json values
    setup = json.load(readFile)
FILEDIR = setup["FILE"]
BOARDWIDTH, BOARDHEIGHT = setup["WIDTH"], setup["HEIGHT"]
DEPTH = setup["SEARCHDEPTH"]

DEFAULTWEIGHT = 5                                                           # default weight for movement

STARTDIR = FILEDIR + "/start.txt"
TARGETSDIR = FILEDIR + "/targets.txt"
AVOIDSDIR = FILEDIR + "/avoids.txt"
SCREENWIDTH, SCREENHEIGHT = 800, ((800 / BOARDWIDTH) * BOARDHEIGHT) + 100   # sets up dimensions for graphics

pygame.init()                                                               # initializes graphics
WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))                  # initializes window
pygame.display.set_caption("Killdozer")                                     # sets title of application
KILLDOZERIMG = pygame.image.load("./images/killdozer.png")                  # creates killdozer image
KILLDOZER = pygame.transform.scale(KILLDOZERIMG, (SCREENWIDTH / BOARDWIDTH, SCREENWIDTH / BOARDWIDTH))  # scales killdozer image


def main():
    if FILEDIR == "random":                                                 # if file is random, create random configuration
        makeRandomInput("random", 15, 60, 1000, 50)
    clock = pygame.time.Clock()                                             # initializes framerate
    run = True                                                              # runs until set false by exiting application
    board = makeBoard()                                                     # initializes matrix

    WIN.fill((200, 200, 200))                                               # fills window with gray
    startBtn = pygame.Rect((SCREENWIDTH / 2) - 50, SCREENWIDTH + 25, 100, 50)   # makes button to press to solve matrix
    pygame.draw.rect(WIN, (180, 180, 180), startBtn)
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    startText = font.render("Start", True, (0, 0, 0))
    startTextRect = startText.get_rect(center=((SCREENWIDTH / 2), SCREENWIDTH + 50))
    WIN.blit(startText, startTextRect)

    drawScore(0)                                                            # draws text for score

    printBoard(board)                                                       # prints the board on the window
    startPos = open(STARTDIR, "r").read().split(",")                        # gets start position of killdozer
    printKillDozer(int(startPos[0]), int(startPos[1]))                      # renders killdozer at start position
    graph = makeGraph(board, getTargets(board, TARGETSDIR, STARTDIR))       # makes a graph out of the matrix

    # printPath(board, graph, (0,0), (8, 6))
    # printPath(board, graph, (8, 6), (0, 2))
    # for g in graph:
    #     print(f"from {g}:")
    #     for p in graph[g]:
    #         print(f"{p}: {graph[g][p]}")
    while run:                                                              # main application loop
        onStart = False
        clock.tick(60)                                                      # sets framerate to 60fps
        mouse = pygame.mouse.get_pos()
        if (SCREENWIDTH / 2) - 50 <= mouse[0] <= (SCREENWIDTH / 2) + 50\
                and SCREENWIDTH + 25 <= mouse[1] <= SCREENWIDTH + 75:       # checks if mouse is over start button
            onStart = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                   # exit button on top right
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if onStart:                                                 # if mouse clicked while over start button
                    doPath(board, graph, (int(startPos[0]), int(startPos[1])))  # main algorithm for pathfinding
        pygame.display.update()                                             # update appearance of graphics


def doPath(board, graph, start):                                            # using the graph of the matrix, find order
    path = findPathOrder(graph, start, DEPTH)
    score = 0
    for i in range(len(path) - 1):
        score = printPath(board, graph, path[i], path[i+1], score)          # print next movement and update score


def printKillDozer(x, y):                                                   # prints killdozer at location
    tileWidth = SCREENWIDTH / BOARDWIDTH
    WIN.blit(KILLDOZER, (x * tileWidth, y * tileWidth))


def makeBoard():                                                            # creates board object
    board = Board(BOARDHEIGHT, BOARDWIDTH, DEFAULTWEIGHT, targetsDir=TARGETSDIR, avoidsDir=AVOIDSDIR)
    return board


def printBoard(board):                                                      # prints board graphics
    tileWidth = SCREENWIDTH / BOARDWIDTH
    background = pygame.Rect(0, 0, SCREENWIDTH, tileWidth * BOARDHEIGHT)
    pygame.draw.rect(WIN, (100, 100, 100), background)
    borderWidth = tileWidth * 0.02
    drawnWidth = tileWidth - 2 * borderWidth
    matrix = board.matrix
    for i, row in enumerate(matrix):
        for j, tile in enumerate(row):
            drawnTile = pygame.Rect((tileWidth * j) + borderWidth, (tileWidth * i) + borderWidth,  drawnWidth, drawnWidth)
            color = (200, 200, 200)
            printedText = ""
            textColor = (0, 0, 0)
            if tile.status == "TARGET":
                color = (0, 120, 0)
                textColor = (250, 200, 80)
                printedText = str(tile.score)
            elif tile.status == "AVOID":
                color = (120, 0, 0)
                printedText = "-" + str(tile.weight)
                textColor = (255, 200, 200)
            elif tile.status == "PATH":
                color = (0, 0, 120)

            font = pygame.font.Font(pygame.font.get_default_font(), int(tileWidth / 4))
            text = font.render(printedText, True, textColor)
            text_rect = text.get_rect(center=((tileWidth * j) + tileWidth / 2, tileWidth * i + tileWidth / 2))

            pygame.draw.rect(WIN, color, drawnTile)
            WIN.blit(text, text_rect)


def reprint(tile):                                                          # updates only the tiles that were affected
    tileWidth = SCREENWIDTH / BOARDWIDTH
    borderWidth = tileWidth * 0.01
    drawnWidth = tileWidth - 2 * borderWidth
    drawnTile = pygame.Rect((tileWidth * tile.x) + borderWidth, (tileWidth * tile.y) + borderWidth, drawnWidth,
                            drawnWidth)
    color = (200, 200, 200)
    printedText = ""
    textColor = (0, 0, 0)
    if tile.status == "TARGET":
        color = (0, 120, 0)
        textColor = (250, 200, 80)
        printedText = str(tile.score)
    elif tile.status == "AVOID":
        color = (120, 0, 0)
        printedText = "-" + str(tile.weight)
        textColor = (255, 200, 200)
    elif tile.status == "PATH":
        color = (0, 0, 120)

    font = pygame.font.Font(pygame.font.get_default_font(), int(tileWidth / 4))
    text = font.render(printedText, True, textColor)
    text_rect = text.get_rect(center=((tileWidth * tile.x) + tileWidth / 2, tileWidth * tile.y + tileWidth / 2))

    pygame.draw.rect(WIN, color, drawnTile)
    WIN.blit(text, text_rect)


def printPath(board, graph, source, dest, score):
    kdx = 0
    kdy = 0
    printBoard(board)  # refreshes board
    for tilePos in graph[source][dest]["PATH"]:
        tile = board.matrix[tilePos[1]][tilePos[0]]
        score -= tile.weight
        score += tile.score
        tile.score = 0
        drawScore(score)
        if tile.status == "DEFAULT":
            tile.status = "PATH"
        reprint(tile)
        printKillDozer(tilePos[0], tilePos[1])
        pygame.display.update()
        time.sleep(0.3)
        reprint(tile)
        kdx = tile.x
        kdy = tile.y
    printKillDozer(kdx, kdy)
    return score


def drawScore(score):
    scoreText = pygame.Rect(25, SCREENWIDTH + 25, 150, 50)
    pygame.draw.rect(WIN, (180, 180, 180), scoreText)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    startText = font.render(f"Score: {score}", True, (0, 0, 0))
    startTextRect = startText.get_rect(center=(0, SCREENWIDTH + 50), left=30)
    WIN.blit(startText, startTextRect)


def makeRandomInput(name, targetCount, avoidCount, maxTarget, maxAvoid):
    if not os.path.exists(name):
        os.mkdir(name)
    places = []
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            places.append((i, j))
    spots = random.sample(places, targetCount + avoidCount + 1)
    targets = ""
    avoids = ""
    targetPlaces = spots[0:targetCount]
    avoidPlaces = spots[targetCount:-1]
    start = spots[-1]
    # print(targetPlaces)
    # print(avoidPlaces)
    # print(start)
    for t in targetPlaces:
        targets += f"{t[0]},{t[1]},{random.randint(0, maxTarget)}\n"
    for a in avoidPlaces:
        avoids += f"{a[0]},{a[1]},{random.randint(10, maxAvoid)}\n"
    start = f"{start[0]},{start[1]}"
    with open(name + "/targets.txt", "w") as f:
        f.write(targets[:-1])
    with open(name + "/avoids.txt", "w") as f:
        f.write(avoids[:-1])
    with open(name + "/start.txt", "w") as f:
        f.write(start)


if __name__ == "__main__":
    main()
