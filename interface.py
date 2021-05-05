import tkinter as tk
from main import Map
from PIL import ImageTk

import numpy as np
import matplotlib.pyplot as plt
from random import seed, randint


# Interface graphique du projet
class InterfaceProject:
    def __init__(self, master):
        # Création de la fenêtre
        self.master = master
        self.map = None
        self.data = None

        # Label
        self.propagate_label = tk.Label(window, text="Project: Procedural Generation")
        self.propagate_label.pack()

        # Definition de la taille de l'image
        self.label_generation_seed = tk.Label(window, text="Generation Seed")
        self.var = tk.StringVar()
        self.var.set(randint(0, 1000))
        self.generation_seed = tk.Spinbox(window, from_=1, to=1000, increment=1, textvariable=self.var)
        self.label_generation_seed.pack()
        self.generation_seed.pack()

        # Definition de la taille de l'image
        self.label_im_width = tk.Label(window, text="Width")
        self.im_width = tk.Spinbox(window, from_=100, to=1000, increment=50)
        self.label_im_width.pack()
        self.im_width.pack()

        self.label_im_height = tk.Label(window, text="Height")
        self.im_height = tk.Spinbox(window, from_=100, to=900, increment=50)
        self.label_im_height.pack()
        self.im_height.pack()

        # Nombre de node au départ
        self.label_seed_number = tk.Label(window, text="Seed Number")
        self.seed_number = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_seed_number.pack()
        self.seed_number.pack()

        # Lissage du flou du Gausse
        self.label_blur = tk.Label(window, text="Blur")
        self.blur = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_blur.pack()
        self.blur.pack()

        # Boutons
        self.button_propagate = tk.Button(window, text="New Map", command=self.propagate_method)
        self.button_propagate.pack()

        # Label Etat du programme
        self.state_label = tk.Label(window, text="No Map Loaded")
        self.state_label.pack()

        self.button_graph_2d = tk.Button(window, text="graph_2D", command=self.show_graph_2d)
        self.button_graph_2d.pack()

        self.button_graph_3d = tk.Button(window, text="graph_3D", command=self.show_graph_3d)
        self.button_graph_3d.pack()

    def propagate_method(self):
        self.state_label.configure(text="Loading Map")
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
        self.map = map_propagate_method.start() # Création de l'image
        self.state_label.configure(text="New Map Loaded")
        self.var.set(randint(0, 1000))

    def show_graph_3d(self):
        if self.map is not None:
            plt.close()
            x = np.arange(0, self.data["width"], 1)
            y = np.arange(0, self.data["height"], 1)
            X, Y = np.meshgrid(x, y)
            Z = self.map
            ax = plt.axes(projection='3d')
            fig = ax.plot_surface(X, Y, Z, cmap="terrain", vmin=0, vmax=400)
            ax.set_title("Carte topographique 3D. Paramètres: \n seed = " + str(self.data["generation_seed"])+" , dimension = "+str(self.data["height"])+"x"+str(self.data["width"])+" , seed_number = "+str(self.data["seed_number"])+" , blur = "+str(self.data["blur"]) )
            plt.colorbar(fig)
            plt.show()

    def show_graph_2d(self):
        if self.map is not None:
            plt.close()
            x = np.arange(0, self.data["width"], 1)
            y = np.arange(0, self.data["height"], 1)
            X, Y = np.meshgrid(x, y)
            Z = self.map
            ax = plt.axes()
            fig = ax.contourf(X, Y, Z, cmap="terrain", vmin=0, vmax=400)
            ax.set_title("Carte topographique 2D. Paramètres: \n seed = " + str(self.data["generation_seed"])+" , dimension = "+str(self.data["height"])+"x"+str(self.data["width"])+" , seed_number = "+str(self.data["seed_number"])+" , blur = "+str(self.data["blur"]) )
            plt.colorbar(fig)
            plt.show()


window = tk.Tk()
project = InterfaceProject(window)
window.mainloop()
