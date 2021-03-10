from random import randint, choice
from PIL import Image
from copy import deepcopy
import timeit

max_height = 200
min_height = -100
empty_node = None


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
        self.height = empty_node


class Map:
    def __init__(self, data):
        self.width = data["width"]
        self.height = data["height"]
        self.seed = data["seed"]
        self.seed_range = 0
        self.map = []
        self.img_map = Image.new("RGB", (self.width, self.height), 0)
        self.seed_list = []
        self.running = True

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

    def is_finished(self):
        self.running = False
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x].height == empty_node:
                    self.running = True

    def propagate(self):
        while self.running:
            self.seed_range += 1
            node_to_check = deepcopy(self.seed_list)
            while len(node_to_check) != 0:
                node = choice(node_to_check)
                near_nodes = []
                for ybis in range(node[0] - self.seed_range, node[0] + self.seed_range + 1):
                    for xbis in range(node[1] - self.seed_range, node[1] + self.seed_range + 1):
                        if 0 <= ybis < self.height and 0 <= xbis < self.width and not (ybis == node[0] and xbis == node[1]):
                            if self.map[ybis][xbis].height == empty_node:
                                near_nodes.append((ybis, xbis))
                if len(near_nodes) == 0:
                    self.seed_list.remove(node)
                while len(near_nodes) != 0:
                    new_node = choice(near_nodes)
                    value = 0
                    close_node = 0
                    for ybis in range(new_node[0] - 1, new_node[0] + 2):
                        for xbis in range(new_node[1] - 1, new_node[1] + 2):
                            if 0 <= ybis < self.height and 0 <= xbis < self.width and not (ybis == new_node[0] and xbis == new_node[1]):
                                if self.map[ybis][xbis].height != empty_node:
                                    value += self.map[ybis][xbis].height
                                    close_node += 1
                    self.map[new_node[0]][new_node[1]].height = round(value/close_node)
                    near_nodes.remove(new_node)
                node_to_check.remove(node)
            self.is_finished()

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
