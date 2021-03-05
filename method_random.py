from random import randint
from PIL import Image


max_height = 250
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
    (225, 250): (111, 43, 43),
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
                self.map[y][x].height = randint(min_height, max_height)

    def filter(self):
        for y in range(self.height):
            for x in range(self.width):
                if 0 < y < self.height-1 and 0 < x < self.width-1:
                    square = 0
                    for xbis in range(x-1,x+2):
                        for ybis in range(y-1,y+2):
                            square += self.map[ybis][xbis].height
                    self.map[y][x].height = round(square/9)
                for color in color_panel.keys():
                    if color[0] < self.map[y][x].height <= color[1]:
                        self.img_map.putpixel((x,y), color_panel[color])
                        break
        self.img_map.show()

    def start(self):
        self.init_map()
        self.filter()
        self.filter()

test = Map()
test.start()
