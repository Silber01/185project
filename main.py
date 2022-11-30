import pygame
from boardData import *
from findpath import *


BOARDWIDTH, BOARDHEIGHT = 20, 20
SCREENWIDTH, SCREENHEIGHT = 800, ((800 / BOARDWIDTH) * BOARDHEIGHT) + 100
DEFAULTWEIGHT = 5
pygame.init()
WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Killdozer")
KILLDOZERIMG = pygame.image.load("./images/killdozer.png")
KILLDOZER = pygame.transform.scale(KILLDOZERIMG, (SCREENWIDTH / BOARDWIDTH, SCREENWIDTH / BOARDWIDTH))


def main():
    clock = pygame.time.Clock()
    run = True
    board = makeBoard()
    printBoard(board, WIN)
    startPos = open("input/start.txt", "r").read().split(",")
    findPath(board, 0, 0)
    printKillDozer(int(startPos[0]), int(startPos[1]))
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


def printKillDozer(x, y):
    tileWidth = SCREENWIDTH / BOARDWIDTH
    WIN.blit(KILLDOZER, (x * tileWidth, y * tileWidth))


def makeBoard():
    board = Board(BOARDHEIGHT, BOARDWIDTH, DEFAULTWEIGHT, targetsDir="./input/targets.txt", avoidsDir="./input/avoids.txt")
    return board


def printBoard(board, WIN):
    tileWidth = SCREENWIDTH / BOARDWIDTH
    background = pygame.Rect(0, 0, SCREENWIDTH, tileWidth * BOARDHEIGHT)
    pygame.draw.rect(WIN, (100, 100, 100), background)
    borderWidth = tileWidth * 0.01
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


if __name__ == "__main__":
    main()