import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

matplotlib.use("TkAgg")

class Plot:
    def __init__(self, title, xlabel, ylabel, y):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(y)
        plt.show()

