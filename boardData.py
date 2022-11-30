class Board:
    def __init__(self, width, height, defaultWeight, targetsDir, avoidsDir):
        self.width = width
        self.height = height
        self.matrix = []
        for row in range(height):
            tileRow = []
            for tile in range(width):
                tileRow.append(Tile(defaultWeight, "DEFAULT"))
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
                    self.matrix[x][y].setScore(weight)
                elif status == "AVOID":
                    self.matrix[x][y].setWeight(weight)
                self.matrix[int(tData[0])][int(tData[1])].setStatus(status)

        targets = open(targetsDir, "r").read().split("\n")
        setTargets(targets, "TARGET")
        targets = open(avoidsDir, "r").read().split("\n")
        setTargets(targets, "AVOID")


class Tile:
    def __init__(self, weight, status, score=0):
        self.weight = weight
        self.status = status
        self.score = score

    def setWeight(self, weight):
        self.weight = weight

    def setStatus(self, status):
        self.status = status

    def setScore(self, score):
        self.score = score

