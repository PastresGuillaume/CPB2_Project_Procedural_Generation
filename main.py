from random import randint
from PIL import Image


max_height = 200
min_height = -100

color_panel = {
    (-100, -75): (0, 15, 198),
    (-75, -50): (0, 93, 255),
    (-50, -25):  (0, 162, 255),
    (-25, 0): (0, 228, 255),
    (0, 25):  (38, 131, 0),
    (25, 50): (51, 178, 0),
    (50, 75): (73, 255, 0),
    (75, 100): (174, 255, 0),
    (100, 125): (236, 255, 0),
    (125, 150): (255, 205, 0),
    (150, 175): (255, 151, 0),
    (175, 200): (255, 73, 0),
    (200, 225): (255, 0, 0),
    (225, 255): (111, 43, 43),
}


class Case:
    def __init__(self):
        self.height = 0


class Map:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.map = []
        self.img_map = Image.new("RGB", (self.width, self.height), 0)

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
                    if round(square/15) < 1:
                        al = randint(-1, 1)
                    else:
                        al = randint(round(-square/15), round(square/15))
                    self.map[y][x].height = round(square/3 + al)
                    if self.map[y][x].height > max_height:
                        self.map[y][x].height = max_height
                    elif self.map[y][x].height < min_height:
                        self.map[y][x].height = min_height
                else:
                    if x != 0 and (y == 0 or y == self.height):
                        self.map[y][x].height = self.map[y][x-1].height + round(1/5*randint(min_height, max_height))
                        if self.map[y][x].height > max_height:
                            self.map[y][x].height = max_height
                        elif self.map[y][x].height < min_height:
                            self.map[y][x].height = min_height
                    else:
                        self.map[y][x].height = self.map[y-1][x].height
                for color in color_panel.keys():
                    if color[0] < self.map[y][x].height <= color[1]:
                        self.img_map.putpixel((x,y), color_panel[color])
        self.img_map.show()

    def start(self):
        self.init_map()
        self.propagate()


