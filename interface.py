import tkinter as tk
from main import Map
from PIL import ImageTk

# définition de la taille de base du canvas
canvas_height = 100
canvas_width = 100


# Interface graphique du projet
class InterfaceProject:
    def __init__(self, master):
        # Création de la fenêtre et du canvas image
        self.master = master
        self.canvas = tk.Canvas(self.master, height=canvas_height, width=canvas_width)
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image='')
        self.image_canvas = ''

        # Label
        self.propagate_label = tk.Label(window, text="Génération par propagation")
        self.propagate_label.pack()

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
        self.label_seed = tk.Label(window, text="Seed Number")
        self.seed = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_seed.pack()
        self.seed.pack()

        # Lissage du flou du Gausse
        self.label_blur = tk.Label(window, text="Blur")
        self.blur = tk.Scale(window, from_=1, to=10, orient="horizontal")
        self.label_blur.pack()
        self.blur.pack()

        # Boutons
        self.button_propagate = tk.Button(window, text="Start", command=self.propagate_method)
        self.button_propagate.pack()

    def propagate_method(self):
        # Récupération des données sélectionnées
        data = {
            "width": int(self.im_width.get()),
            "height":  int(self.im_height.get()),
            "seed": int(self.seed.get()),
            "blur": int(self.blur.get()),
        }
        map_propagate_method = Map(data) # Envoi des données
        self.image = map_propagate_method.start() # Création de l'image
        self.show_image() # Affichage de l'image

    def show_image(self):
        # Affiche l'image générée dans le canvas de tkinter
        self.image_canvas = ImageTk.PhotoImage(self.image)
        height = self.image.height
        width = self.image.width
        self.canvas.config(height=height, width=width)
        self.canvas.itemconfig(self.canvas_image, image = self.image_canvas)


window = tk.Tk()
project = InterfaceProject(window)
window.mainloop()
