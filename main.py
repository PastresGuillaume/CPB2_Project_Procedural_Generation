from random import randint
from PIL import Image


max_height = 200
min_height = -55


class Case:
    def __init__(self):
        self.height = 0


class Map:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.map = []
        self.img_map = Image.new("L", (self.width, self.height), 0)

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.map[y][x].height, end="; ")
            print("")

    def init_map(self):
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(Case())
        self.map[0][0].height = randint(min_height, max_height)

    def propagate(self):
        for y in range(self.height):
            for x in range(self.width):
                if 0 < y < self.height-1 and 0 < x < self.width-1:
                    square = self.map[y-1][x-1].height + self.map[y-1][x].height + self.map[y][x-1].height
                    if round(square/45) < 1:
                        al = randint(-1, 1)
                    else:
                        al = randint(round(-square/15), round(square/15))
                    self.map[y][x].height = round(square/3 + al)
                    if self.map[y][x].height > 200:
                        self.map[y][x].height = 200
                    elif self.map[y][x].height < -55:
                        self.map[y][x].height = -55
                else:
                    self.map[y][x].height = randint(min_height, max_height)
                self.img_map.putpixel((x,y), self.map[y][x].height + 55)
        self.img_map.show()


test = Map()
test.init_map()
test.propagate()
