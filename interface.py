# Importation des Modules
import tkinter as tk
import matplotlib.pyplot as plt

import numpy as np
from random import seed, randint

from main import Map


# Interface graphique du projet
class InterfaceProject:
    def __init__(self, master):
        # Création de la fenêtre
        self.master = master
        self.map = None
        self.data = None

        # Label
        self.propagate_label = tk.Label(window, text="Project: Procedural Generation")
        self.propagate_label.grid(row=0, columnspan=2)

        # Definition de la taille de l'image
        self.label_generation_seed = tk.Label(window, text="Generation Seed")
        self.var = tk.StringVar()
        self.var.set(randint(0, 1000)) # Genere une seed aléatoire au début
        self.generation_seed = tk.Spinbox(window, from_=1, to=1000, increment=1, textvariable=self.var)
        self.label_generation_seed.grid(row=1, columnspan=2)
        self.generation_seed.grid(row=2, columnspan=2)

        # Definition de la taille de l'image
        self.label_im_width = tk.Label(window, text="Width")
        self.im_width = tk.Spinbox(window, from_=100, to=1000, increment=50)
        self.label_im_width.grid(row=3, column=0)
        self.im_width.grid(row=4, column=0)

        self.label_im_height = tk.Label(window, text="Height")
        self.im_height = tk.Spinbox(window, from_=100, to=900, increment=50)
        self.label_im_height.grid(row=3, column=1)
        self.im_height.grid(row=4, column=1)

        # Nombre de node au départ
        self.label_seed_number = tk.Label(window, text="Seed Number")
        self.seed_number = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_seed_number.grid(row=5, column=0)
        self.seed_number.grid(row=6, column=0)

        # Lissage du flou du Gausse
        self.label_blur = tk.Label(window, text="Blur")
        self.blur = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_blur.grid(row=5, column=1)
        self.blur.grid(row=6, column=1)

        # Label Etat du programme
        self.state_label = tk.Label(window, text="No Map Generated")
        self.state_label.grid(row=8, columnspan=2)

        # Boutons
        self.button_propagate = tk.Button(window, text="New Map", command=self.propagate_method)
        self.button_propagate.grid(row=7, columnspan=2)

        self.button_graph_2d = tk.Button(window, text="graph_2D", command=self.show_graph_2d)
        self.button_graph_2d.grid(row=9, column=0)

        self.button_graph_3d = tk.Button(window, text="graph_3D", command=self.show_graph_3d)
        self.button_graph_3d.grid(row=9, column=1)

    def propagate_method(self):
        self.state_label.configure(text="Generating Map")
        self.master.update()
        # Récupération des données sélectionnées
        self.data = {
            "width": int(self.im_width.get()),
            "height":  int(self.im_height.get()),
            "seed_number": int(self.seed_number.get()),
            "blur": int(self.blur.get()),
            "generation_seed": int(self.generation_seed.get())
        }
        seed(self.data["generation_seed"])
        map_propagate_method = Map(self.data) # Envoi des données
        self.map = map_propagate_method.start() # Création de la carte
        self.state_label.configure(text="New Map Generated")
        self.var.set(randint(0, 1000)) # Génère une nouvelle seed aléatoire

    def show_graph_2d(self):
        # Affiche la carte en 2D
        if self.map is not None:
            plt.close() # Ferme la fenetre s'il y en a deja une
            x = np.arange(0, self.data["width"], 1)
            y = np.arange(0, self.data["height"], 1)
            X, Y = np.meshgrid(x, y) # crée le plan de la carte
            Z = self.map # recupere la hauteur en fonction de la position
            ax = plt.axes()
            ax.set_xlim(0, int(self.data["width"]))
            ax.set_ylim(0, int(self.data["height"]))
            ax.set_aspect(True) # Désactive le changement d'échelle des axes
            fig = ax.contourf(X, Y, Z, cmap="terrain", vmin=0, vmax=400)
            ax.set_title("Carte topographique 2D. Paramètres: \n seed = " + str(self.data["generation_seed"])+" , dimension = "+str(self.data["height"])+"x"+str(self.data["width"])+" , seed_number = "+str(self.data["seed_number"])+" , blur = "+str(self.data["blur"]) )
            plt.colorbar(fig) # Légende
            plt.show()

    def show_graph_3d(self):
        # Affiche la carte en 3D
        if self.map is not None:
            plt.close()
            x = np.arange(0, self.data["width"], 1)
            y = np.arange(0, self.data["height"], 1)
            X, Y = np.meshgrid(x, y)
            Z = self.map
            ax = plt.axes(projection='3d')
            ax.set_box_aspect((int(self.data["width"]),int(self.data["height"]), 400))
            ax.invert_xaxis()
            fig = ax.plot_surface(X, Y, Z, cmap="terrain", vmin=0, vmax=400)
            ax.set_title("Carte topographique 3D. Paramètres: \n seed = " + str(self.data["generation_seed"])+" , dimension = "+str(self.data["height"])+"x"+str(self.data["width"])+" , seed_number = "+str(self.data["seed_number"])+" , blur = "+str(self.data["blur"]) )
            plt.colorbar(fig)
            plt.show()


window = tk.Tk()
project = InterfaceProject(window)
window.mainloop()
