import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()

plt.show(block=False)


def plot(scores, mean_scores):
    ax.clear()
    ax.set_title("Training...")
    ax.set_xlabel("Number of games")
    ax.set_ylabel("Score")
    ax.scatter(range(len(scores)), scores, c="orange")
    ax.plot(mean_scores)
    ax.set_ylim(ymin=0)
    ax.text(len(scores)-1, scores[-1], str(scores[-1]))
    ax.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    
    fig.canvas.draw()
    fig.canvas.flush_events()