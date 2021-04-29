from random import randint, choice
from PIL import Image

min_height = 0
max_height = 400
empty_node = None # valeur des cases vides
added_node = 999  # valeur des cases vides qui ont été ajoutées à la liste des cases à s'occuper

# Panel de couleur utlisée au départ
color_panel1 = {
    (-1, 25): (0, 15, 198),
    (25, 50): (0, 93, 255),
    (50, 75):  (0, 162, 255),
    (75, 100): (0, 228, 255),
    (100, 125):  (38, 131, 0),
    (125, 150): (51, 178, 0),
    (150, 175): (73, 255, 0),
    (175, 200): (174, 255, 0),
    (200, 225): (236, 255, 0),
    (225, 250): (255, 205, 0),
    (250, 275): (255, 151, 0),
    (275, 300): (255, 73, 0),
    (300, 325): (255, 0, 0),
    (325, 350): (111, 43, 43),
}

# Panel de couleur réduit
color_panel2 = {
    (-1, 40): (0, 15, 198),
    (40, 80): (0, 93, 255),
    (80, 120):  (0, 162, 255),
    (120, 160):  (38, 131, 0),
    (160, 200): (73, 255, 0),
    (200, 240): (174, 255, 0),
    (240, 280): (236, 255, 0),
    (280, 320): (255, 151, 0),
    (320, 360): (255, 0, 0),
    (360, 400): (111, 43, 43),
}


class Case:
    def __init__(self):
        self.height = empty_node


class Map:
    def __init__(self, data):
        # Récupération des données envoyées
        self.width = data["width"]
        self.height = data["height"]
        self.seed = data["seed"]
        self.map = []
        self.img_map = Image.new("RGB", (self.width, self.height), 0)
        self.seed_list = []
        self.node_list = []

    def show(self):
        # Print la valeur numérique de chaque case (pour test uniquement)
        for y in range(self.height):
            for x in range(self.width):
                print(self.map[y][x].height, end="; ")
            print("")

    def init_map(self):
        # Création d'une matrice de la taille souhaitée
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(Case())

    def node_spawn(self):
        # Ajoute le nombre de seed demandées sur la carte (Position et hauteur aléatoire)
        while len(self.seed_list) < self.seed:
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
            if self.map[y][x].height == empty_node:  # On vérifie que la case est vide
                self.map[y][x].height = randint(min_height, max_height)
                self.seed_list.append((y, x))

    def check_close_node(self, node):
        # Ajoute toute les nodes qui n'ont pas encore étés sélectionnés autour du point considéré, dans une liste
        for ybis in range(node[0] - 1, node[0] + 2):
            for xbis in range(node[1] - 1, node[1] + 2):
                if 0 <= ybis < self.height and 0 <= xbis < self.width and self.map[ybis][xbis].height == empty_node:
                    self.node_list.append((ybis,xbis))
                    self.map[ybis][xbis].height = added_node

    def propagate(self):
        i = 0
        iterations = 3 + 1
        for seed in self.seed_list:
            self.check_close_node(seed)
            i += 1
        while len(self.node_list) !=0:
            new_node = choice(self.node_list)
            square = 0
            close_node = 0
            for radius in range(1, iterations):
                for ybis in range(new_node[0] - radius, new_node[0] + radius + 1):
                    for xbis in range(new_node[1] - radius, new_node[1] + radius + 1):
                        if 0 <= ybis < self.height and 0 <= xbis < self.width and (xbis ==new_node[1]-radius or xbis == new_node[1]+radius or ybis==new_node[0]-radius or ybis== new_node[0]+radius )and self.map[ybis][xbis].height != added_node:
                            if self.map[ybis][xbis].height != empty_node:
                                square += self.map[ybis][xbis].height*(iterations-radius)
                                close_node += 1*(iterations-radius)
            #perc = abs(round(1 / 5 * square / close_node))
            perc = round(max_height * 0.05)
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
        # Convertit la valeur numérique des hauteur en couleur (selon un panel de couleur
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x].height == empty_node:
                    self.img_map.putpixel((x, y), (0, 0, 0))
                else:
                    for color in color_panel2.keys():
                        if color[0] < self.map[y][x].height <= color[1]:
                            self.img_map.putpixel((x,y), color_panel2[color])

    def start(self):
        self.init_map()
        self.node_spawn()
        self.propagate()
        self.convert_image()
        return self.img_map

