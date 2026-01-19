import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, FFMpegWriter


# TODO: Make these variables imported from game_logic.py
colorGreen = (0.6758, 0.7969, 0.375)
colorDarkGreen = (0.1680, 0.1992, 0.09375)

cell_size = 30
cell_count = 20
window_size = cell_size * cell_count


frames_data = [
        [(4, 1), (3, 1), (2, 1)], 
        [(4, 2), (4, 1), (3, 1)]
]


fig, ax = plt.subplots()

ax.set_xlim(0, window_size)
ax.set_ylim(0, window_size)
ax.set_box_aspect(1)
ax.set_axis_off()

background = patches.Rectangle((0, 0), window_size, window_size, linewidth=1, edgecolor=colorGreen, facecolor=colorGreen, zorder=0)
ax.add_patch(background)

max_snake_len = max(len(frame) for frame in frames_data)
body_patches = []

for _ in range(max_snake_len):
    rect = patches.Rectangle((0, 0), cell_size, cell_size, facecolor=colorDarkGreen, zorder = 1)
    rect.set_visible(False)
    ax.add_patch(rect)
    body_patches.append(rect)


def update_body(frame_idx):
    body_coords = frames_data[frame_idx]

    for i, rect in enumerate(body_patches):
        if i < len(body_coords):
            x, y = body_coords[i]
            rect.set_xy((x * cell_size, y * cell_size))
            rect.set_visible(True)
        else:
            rect.set_visible(False)


    return body_patches

anim = FuncAnimation(
    fig,
    update_body,
    frames=len(frames_data),
    interval=200,
    blit=True
)

writer = FFMpegWriter(fps = 5)
anim.save("test_animation.mp4", writer=writer)

plt.close()