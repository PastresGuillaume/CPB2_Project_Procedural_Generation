import tkinter as tk
from main import Map

map_test = Map()


window = tk.Tk()
window.title("Projet CPB2")


canvas = tk.Canvas(window, bg="black", width=300, height=300)
canvas.pack()

propagate_label = tk.Label(window, text="Génération par propagation")
propagate_label.pack()

button1 = tk.Button(window, text="Start", command=map_test.start)
button1.pack()


window.mainloop()
