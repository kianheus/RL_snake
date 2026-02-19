import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class TrainingPlotter():

    def __init__(self):
        print("Matplotlib backend:", matplotlib.get_backend())
        self.fig, self.ax = plt.subplots(figsize=(4,3))
        plt.show(block=False)

    def update(self, scores, mean_scores):
        self.ax.clear()
        self.ax.set_title("Training...")
        self.ax.set_xlabel("Number of games")
        self.ax.set_ylabel("Score")

        self.ax.scatter(range(len(scores)), scores, c="orange")
        self.ax.plot(mean_scores)
        self.ax.set_ylim(ymin=0)

        self.ax.text(len(scores)-1, scores[-1], str(scores[-1]))
        self.ax.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()