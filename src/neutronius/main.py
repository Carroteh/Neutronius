from os import truncate
from tkinter.messagebox import showinfo
from tkinter.ttk import Progressbar

import threading
from neutronius.game.Game import Game
import tkinter as tk
from tkinter import ttk

g = Game(500, 500)

def train(episodes, alpha, gamma, epsilon, seed):
    if seed == "":
        return
    def do():
        report = g.train(episodes, alpha, gamma, epsilon, seed)
        showinfo(message=f"Training complete! \n Deaths: {report[0]} \n Electrons Collected: {report[1]} \n High Score: {report[2]}")
    threading.Thread(target=do, daemon=True).start()

def infer(seed):
    if seed == "":
        return
    def do():
        g.infer(seed)
    threading.Thread(target=do, daemon=True).start()

def stop():
    g.stop_training()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Neutronius")
    root.configure()
    root.minsize(380,400)
    root.maxsize(380,400)
    root.geometry("200x200+100+100")

    # Inputs
    tk.Label(root, text="Epsilon", font=("New Times Roman", 11)).grid(column=0, row=1, padx=20, pady=1, sticky=tk.S)
    scale_eps = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=150)
    scale_eps.set(0.2)
    scale_eps.grid(column=0, row=2, pady=1, padx=10)

    tk.Label(root, text="Gamma", font=("New Times Roman", 11)).grid(column=0, row=3, padx=10, pady=1, sticky=tk.S)
    scale_gamma = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=150)
    scale_gamma.set(0.9)
    scale_gamma.grid(column=0, row=4, pady=1, padx=10)

    tk.Label(root, text="Alpha", font=("New Times Roman", 11)).grid(column=0, row=5, padx=10, pady=1, sticky=tk.S)
    scale_alpha = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=150)
    scale_alpha.set(0.2)
    scale_alpha.grid(column=0, row=6, padx=10, pady=1)

    tk.Label(root, text="Seed", font=("New Times Roman", 11)).grid(column=0, row=7, padx=10, pady=1, sticky=tk.S)
    seed = tk.Entry(root, font=("Helvetica", 11))
    seed.grid(column=0, row=8, pady=1, padx=10)

    tk.Label(root, text="Episodes", font=("New Times Roman", 11)).grid(column=0, row=9, padx=10, pady=1, sticky=tk.S)
    episodes = tk.Scale(root, from_=10, to=10000000, resolution=1, orient=tk.HORIZONTAL, length=150)
    episodes.set(1000000)
    episodes.grid(column=0, row=10, pady=1, padx=10)


    # Buttons

    tk.Button(root, width=20, height=1, text="Train", command=lambda: train(episodes.get(), scale_alpha.get(), scale_gamma.get(), scale_eps.get(), seed.get())).grid(column=1, row=1, padx=10, pady=10)
    pb = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=150, mode='determinate')
    g.set_pb(pb)
    pb.grid(column=1, row=2, padx=10, pady=10)
    tk.Button(root, width=20, height=1 ,text="Infer", command=lambda: infer(seed.get())).grid(column=1, row=3, padx=10, pady=10)
    tk.Button(root, width=20, height=1, text="Stop", command=lambda: stop()).grid(column=1, row=4, padx=10, pady=10)

    root.mainloop()

 