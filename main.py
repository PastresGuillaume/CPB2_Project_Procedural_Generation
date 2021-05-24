# Importation des Modules
from random import randint, choice
from math import sqrt
import numpy as np

from scipy.ndimage.filters import gaussian_filter

min_height = 0
max_height = 400
empty_node = None # valeur des cases vides
added_node = 999  # valeur des cases vides qui ont été ajoutées à la liste des cases à traiter


def get_distance(node, seed):
    # retourne le module de la distance entre 2 points
    return sqrt((seed[0] - node[0]) ** 2 + (seed[1] - node[1]) ** 2)


class Map:
    def __init__(self, data):
        # Récupération des données envoyées
        self.width = data["width"]
        self.height = data["height"]
        self.seed = data["seed_number"]
        self.blur = data["blur"]
        self.map = []
        self.seed_list = []
        self.node_list = []
        self.var = round(max_height * 0.10)

    def show(self):
        # Print la valeur numérique de chaque case (pour tester uniquement)
        for y in range(self.height):
            for x in range(self.width):
                print(self.map[y][x], end="; ")
            print("")

    def init_map(self):
        # Création d'une matrice de la taille souhaitée
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(empty_node)

    def node_spawn(self):
        # Ajoute le nombre de seed demandées sur la carte (Position et hauteur aléatoire)
        while len(self.seed_list) < self.seed:
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
            if self.map[y][x] == empty_node:  # On vérifie que la case est vide
                height = randint(min_height, max_height)
                self.map[y][x] = height
                self.seed_list.append([y, x, height])

    def check_close_node(self, node):
        # Ajoute toute les nodes qui n'ont pas encore été sélectionnées autour du point considéré dans une liste
        for ybis in range(node[0] - 1, node[0] + 2):
            for xbis in range(node[1] - 1, node[1] + 2):
                if 0 <= ybis < self.height and 0 <= xbis < self.width and self.map[ybis][xbis] == empty_node:
                    self.node_list.append((ybis,xbis))
                    self.map[ybis][xbis] = added_node

    def propagate(self):
        # Fonction permettant de propager les points de départs
        i = 0  # Compteur pour connaitre l'avancement du programme
        radius_range = 3 + 1 # Portée de la moyenne (+1 car on commence à 1 de portée)
        for seed in self.seed_list:  # On traite d'abord les seeds
            self.check_close_node(seed)
            i += 1
        while len(self.node_list) !=0:
            new_node = choice(self.node_list)  # On choisit une node aléatoire parmit la liste
            square = 0  # Somme des hauteur
            tendancy = 0  # Somme des hauteur des seeds pondérées par la distance
            close_node = 0  # Compteur du nombre de points pondérés
            seed_weight = 0  # Copteur des pondération des distances des seeds
            for radius in range(1, radius_range):
                for ybis in range(new_node[0] - radius, new_node[0] + radius + 1):
                    for xbis in range(new_node[1] - radius, new_node[1] + radius + 1):
                        if 0 <= ybis < self.height and 0 <= xbis < self.width and (xbis == new_node[1]-radius or xbis == new_node[1]+radius or ybis==new_node[0]-radius or ybis== new_node[0]+radius )and self.map[ybis][xbis] != added_node:
                            if self.map[ybis][xbis] != empty_node:  # si la case regardée n'est pas vide
                                square += self.map[ybis][xbis]*(radius_range-radius) # On ajoute sa hauteur à la somme
                                close_node += 1*(radius_range-radius)  # + 1 * coeff pondération au compteur
            mean_value = round(square / close_node)

            # Pondère la hauteur de toutes les seeds par raport a leur distance avec le point
            for seed in self.seed_list:
                dist = (get_distance(new_node, seed))
                tendancy += seed[2] * 1 / dist
                seed_weight += 1 / dist
            seed_value = round(tendancy / seed_weight)

            final_value = round((19*mean_value + seed_value)/20) + randint(-self.var, self.var)
            if final_value < min_height:
                final_value = min_height
            elif final_value > max_height:
                final_value = max_height

            self.map[new_node[0]][new_node[1]] = final_value  # assigne la valeur au point
            self.check_close_node(new_node)  # ajoute les points adjacents à la liste à traiter
            self.node_list.remove(new_node)
            i += 1
            print(self.width * self.height - i) # affichage du compteur

    def start(self):
        # Lancement de l'algorithme
        self.init_map()
        self.node_spawn()
        self.propagate()
        self.map = gaussian_filter(np.array(self.map), self.blur)  # Atténue les variations
        return self.map

