import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

matplotlib.use("TkAgg")

class Plot:
    def __init__(self):
        self.epsilon = [1.0]
        self.x = [1]
        self.figure, self.ax = plt.subplots()
        self.graph, = self.ax.plot(self.x, self.epsilon, label="Epsilon Decay")
        self.ax.set_title("Epsilon Decay Over Time")
        self.ax.set_xlabel("Time Steps")
        self.ax.set_ylabel("Epsilon")
        self.ax.grid(True)
        self.ax.legend()
        self.epsilon_queue = queue.Queue()
        self.running = True

    def update(self, epsilon):
        """Add epsilon value to the queue."""
        self.epsilon_queue.put(epsilon)

    def animate(self, frame):
        """Update the plot with new epsilon values from the queue."""
        if not self.running:
            return

        # Process all available epsilon values in the queue
        while not self.epsilon_queue.empty():
            try:
                epsilon = self.epsilon_queue.get_nowait()
                self.epsilon.append(epsilon)
                self.x.append(self.x[-1] + 1)
            except queue.Empty:
                break

        # Update the plot data
        self.graph.set_data(self.x, self.epsilon)
        self.ax.relim()
        self.ax.autoscale_view()
        return self.graph,

    def start(self):
        """Start the animation."""
        # Update every 500ms (2 updates per second)
        self.ani = FuncAnimation(self.figure, self.animate, interval=500, blit=False)
        #plt.show(block=False)
        plt.pause(0.001)

    def stop(self):
        """Stop the animation."""
        self.running = False
        self.ani.event_source.stop()
        plt.close(self.figure)