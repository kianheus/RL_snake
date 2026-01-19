import matplotlib.pyplot as plt
import matplotlib.patches as patches


# TODO: Make these variables imported from game_logic.py
colorGreen = (0.6758, 0.7969, 0.375)
colorDarkGreen = (0.1680, 0.1992, 0.09375)

cell_size = 30
cell_count = 20
window_size = cell_size * cell_count

fig, ax = plt.subplots()

background = patches.Rectangle((0, 0), window_size, window_size, linewidth=1, edgecolor=colorGreen, facecolor=colorGreen, zorder=0)

frames = [1]
body_coords = [(4, 1), (3, 1), (2, 1)]

for frame in frames:
    for part_coords in body_coords:
        x = part_coords[0]
        y = part_coords[1]
        sqr_body = patches.Rectangle((x*cell_size, y*cell_size), cell_size, cell_size, linewidth=1, edgecolor=colorDarkGreen, facecolor=colorDarkGreen, zorder = 1)
        ax.add_patch(sqr_body)

ax.add_patch(background)

ax.set_xlim(0, window_size)
ax.set_ylim(0, window_size)
ax.set_box_aspect(1)
ax.set_axis_off()

#plt.savefig("test", bbox_inches="tight", pad_inches=0.0)
plt.show()