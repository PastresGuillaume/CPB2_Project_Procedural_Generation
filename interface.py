import tkinter as tk
from main import Map
from PIL import Image, ImageTk

canvas_height = 100
canvas_width = 100


class InterfaceProject:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, height=canvas_height, width=canvas_width)
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image='')
        self.image_canvas = ''

        # Placements des widgets
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

        # Bouton
        self.button_propagate = tk.Button(window, text="Start", command=self.propagate_method)
        self.button_propagate.pack()

    def propagate_method(self):
        data = {
            "width": int(self.im_width.get()),
            "height":  int(self.im_height.get()),
            "seed": int(self.seed.get()),
        }
        map_propagate_method = Map(data)
        self.image = map_propagate_method.start()
        self.show_image()

    def show_image(self):
        self.image_canvas = ImageTk.PhotoImage(self.image)
        height = self.image.height
        width = self.image.width
        self.canvas.config(height=height, width=width)
        self.canvas.itemconfig(self.canvas_image, image = self.image_canvas)


window = tk.Tk()
project = InterfaceProject(window)
window.mainloop()
