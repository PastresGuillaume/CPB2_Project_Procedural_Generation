import tkinter as tk
from main import Map


def tk_propagate_method():
    data = {
        "width" : int(im_width.get()),
        "height" : int(im_height.get()),
        "seed" : int(seed.get()),
        "seed_range": int(scale_seed_range.get())
    }
    map_propagate_method = Map(data)
    map_propagate_method.start()


window = tk.Tk()
window.title("Projet CPB2")


canvas = tk.Canvas(window, bg="black", width=300, height=300)
canvas.pack()

propagate_label = tk.Label(window, text="Génération par propagation")
propagate_label.pack()

# Interface, paramètres méthode par propagations

# Definition de la taille de l'image
label_im_width = tk.Label(window, text="Width")
im_width = tk.Spinbox(window, from_=100, to=1000, increment =1)
label_im_width.pack()
im_width.pack()

label_im_height = tk.Label(window, text="Height")
im_height = tk.Spinbox(window, from_=100, to=900, increment =1)
label_im_height.pack()
im_height.pack()

# Nombre de node au départ
label_seed = tk.Label(window, text="Seed Number")
seed = tk.Spinbox(window, from_=1, to=1000, increment =1)
label_seed.pack()
seed.pack()

# Range des Seeds
scale_seed_range=tk.Scale(window, orient='horizontal', from_=1, to=9,resolution=1, length=300,label='Seed Range')
scale_seed_range.set(5)
scale_seed_range.pack()


button_propagate = tk.Button(window, text="Start", command=tk_propagate_method)
button_propagate.pack()


window.mainloop()
