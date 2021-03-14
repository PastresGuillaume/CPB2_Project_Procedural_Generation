from random import randint, choice
from PIL import Image


max_height = 255
min_height = -100
empty_node = None


color_panel = {
    (-101, -75): (0, 15, 198),
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
        self.height = empty_node


class Map:
    def __init__(self, data):
        self.width = data["width"]
        self.height = data["height"]
        self.seed = data["seed"]
        self.map = []
        self.img_map = Image.new("RGB", (self.width, self.height), 0)
        self.seed_list = []
        self.node_list = []

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

    def node_spawn(self):
        while len(self.seed_list) < self.seed:
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
            if self.map[y][x].height == empty_node:
                self.map[y][x].height = randint(min_height, max_height)
                self.seed_list.append((y, x))

    def check_close_node(self, node):
        for ybis in range(node[0] - 1, node[0] + 2):
            for xbis in range(node[1] - 1, node[1] + 2):
                if 0 <= ybis < self.height and 0 <= xbis < self.width and (not(ybis,xbis) in self.node_list) and self.map[ybis][xbis].height == empty_node :
                    self.node_list.append((ybis,xbis))

    def propagate(self):
        i = 0
        for seed in self.seed_list:
            self.check_close_node(seed)
            i += 1
        while len(self.node_list) !=0:
            new_node = choice(self.node_list)
            square = 0
            close_node = 0
            for ybis in range(new_node[0] - 1, new_node[0] + 2):
                for xbis in range(new_node[1] - 1, new_node[1] + 2):
                    if 0 <= ybis < self.height and 0 <= xbis < self.width and not (ybis == new_node[0] and xbis == new_node[1]):
                        if self.map[ybis][xbis].height != empty_node:
                            square += self.map[ybis][xbis].height
                            close_node += 1
            perc = abs(round(1 / 5 * square / close_node))
            value = round(square / close_node) + randint(-perc, perc)
            if value < min_height:
                value = min_height
            elif value > max_height:
                value = max_height
            self.map[new_node[0]][new_node[1]].height = value
            self.check_close_node(new_node)
            self.node_list.remove(new_node)
            i +=1
            print(self.width * self.height - i)

    def convert_image(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x].height == empty_node:
                    self.img_map.putpixel((x, y), (0, 0, 0))
                else:
                    for color in color_panel.keys():
                        if color[0] < self.map[y][x].height <= color[1]:
                            self.img_map.putpixel((x,y), color_panel[color])
        self.img_map.show()

    def start(self):
        self.init_map()
        self.node_spawn()
        self.propagate()
        self.convert_image()