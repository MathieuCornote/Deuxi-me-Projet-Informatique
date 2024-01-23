import tkinter as tk
from Data.Data_extractor import Data_extractor

class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("450x200")
        self.root.configure(background="white")
        self.label = tk.Label(self.root, text="Chargement des données en cours...", bg="white", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.progressbar = tk.Canvas(self.root, width=245, height=35, bg='white')
        self.progressbar.pack(pady=10)
        self.root.after(4000, lambda: self.root.destroy())
        self.root.after(100, self.animate_loading)

        self.root.mainloop()

    def animate_loading(self, step=0):
        self.progressbar.delete("all")
        x = 10
        y = 10
        for i in range(10):
            if i == step:
                color = "black"
            else:
                color = "gray"
            self.progressbar.create_rectangle(x, y, x+20, y+20, fill=color)
            x += 30
        step += 1
        if step == 10:
            step = 0
        self.root.after(100, lambda: self.animate_loading(step))