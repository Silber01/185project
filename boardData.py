class Board:
    def __init__(self, height, width, defaultWeight, targetsDir, avoidsDir):
        self.width = width
        self.height = height
        self.matrix = []
        for row in range(height):
            tileRow = []
            for col in range(width):
                tileRow.append(Tile(col, row, defaultWeight, "DEFAULT"))
            self.matrix.append(tileRow)

        def setTargets(targets, status):
            for t in targets:
                tData = t.split(",")
                if len(tData) != 3:
                    print(f"{tData} is not a valid target!")
                    continue
                try:
                    x = int(tData[0])
                    y = int(tData[1])
                    weight = int(tData[2])
                except ValueError:
                    print(f"{tData} is not a valid target!")
                    continue
                if x < 0 or x >= width or y < 0 or y >= height:
                    print(f"{tData} is out of range!")
                    continue
                if status == "TARGET":
                    self.matrix[y][x].setScore(weight)
                elif status == "AVOID":
                    self.matrix[y][x].setWeight(weight)
                self.matrix[y][x].setStatus(status)

        targets = open(targetsDir, "r").read().split("\n")
        setTargets(targets, "TARGET")
        targets = open(avoidsDir, "r").read().split("\n")
        setTargets(targets, "AVOID")
        for y, row in enumerate(self.matrix):
            for x, tile in enumerate(row):
                print(self.matrix[y][x])
                continue



class Tile:
    def __init__(self, x, y, weight, status, score=0, neighbors={}):
        self.x = x
        self.y = y
        self.weight = weight
        self.status = status
        self.score = score
        self.neighbors = neighbors

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, weight: {self.weight}, status: {self.status}, score: {self.score}, "

    def setWeight(self, weight):
        self.weight = weight

    def setStatus(self, status):
        self.status = status

    def setScore(self, score):
        self.score = score

    def setNeighbors(self, neighbors):
        pass



