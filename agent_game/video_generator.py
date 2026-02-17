import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.image as mpimg
import matplotlib
matplotlib.use("Agg")
import os


# TODO: Make these variables imported from game_logic.py
colorGreen = (0.6758, 0.7969, 0.375)
colorDarkGreen = (0.1680, 0.1992, 0.09375)

cell_size = 30
cell_count = 20
window_size = cell_size * cell_count

class Animator():

    def __init__(self, body_data, food_data, target_px=400, dpi=50):
        self.body_data = body_data
        self.food_data = food_data
        self.dpi = dpi

        

        fig_size_in = target_px / dpi  # inches

        self.fig, self.ax = plt.subplots(figsize=(fig_size_in, fig_size_in), dpi=dpi)
        self.ax.set_position([0, 0, 1, 1])
        self.ax.margins(0)

        self.ax.set_xlim(0, window_size)
        self.ax.set_ylim(0, window_size)
        self.ax.set_box_aspect(1)
        self.ax.set_axis_off()

        background = patches.Rectangle((0, 0), window_size, window_size, linewidth=1, edgecolor=colorGreen, facecolor=colorGreen, zorder=0)
        self.ax.add_patch(background)

        
        self.body_patches = []
        self.create_body_patches()

        self.create_food_artist()

    def create_body_patches(self):
        max_snake_len = max(len(frame) for frame in self.body_data)
        for _ in range(max_snake_len):
            #rect = patches.Rectangle((0, 0), cell_size, cell_size, facecolor=colorDarkGreen, zorder = 1)
            rect = patches.FancyBboxPatch(
                        (0, 0),
                        cell_size,
                        cell_size,
                        boxstyle="Round,pad=0.0,rounding_size=3",  # 5 pixels radius, tweak as needed
                        linewidth=0,
                        facecolor=colorDarkGreen,
                        zorder=1
                    )
            
            
            rect.set_visible(False)
            self.ax.add_patch(rect)
            self.body_patches.append(rect)

    def create_food_artist(self):
        food_path = os.path.join("graphics", "food.png")
        food_img = mpimg.imread(food_path)

        food_coord0 = (0, 0)
        self.food_artist = self.ax.imshow(
                               food_img,
                               extent=[
                                   food_coord0[0] * cell_size, (food_coord0[0] + 1) * cell_size,
                                   food_coord0[1] * cell_size, (food_coord0[1] + 1) * cell_size
                               ],
                               zorder=3,
                               interpolation="nearest",
                           )


    def update(self, frame_idx):
        body_coords = self.body_data[frame_idx]
        food_coord = self.food_data[frame_idx]

        for i, rect in enumerate(self.body_patches):
            if i < len(body_coords):
                x, y = body_coords[i]
                #rect.set_xy((x * cell_size, y * cell_size))
                rect.set_bounds(x * cell_size, y * cell_size, cell_size, cell_size)
                rect.set_visible(True)
            else:
                rect.set_visible(False)

        x_food, y_food = food_coord
        self.food_artist.set_extent([
            x_food * cell_size, (x_food + 1) * cell_size,
            y_food * cell_size, (y_food + 1) * cell_size
        ])
        
        # Careful here, only a shallow list copy
        all_patches = self.body_patches + [self.food_artist]
    
        return all_patches

    def make_animation(self, save_path, hold_seconds=1.0, fps=20):
        
        hold_frames = int(hold_seconds * fps)

        frame_indices = list(range(len(self.body_data))) + \
                        [len(self.body_data) - 1] * hold_frames

        anim = FuncAnimation(
                    self.fig,
                    self.update,
                    frames=frame_indices,
                    interval=int(1000/fps),
                    blit=False
                )

        writer = PillowWriter(fps=fps)
        print("saving animation...")
        path = os.path.join(save_path, "best_run_animation.gif")
        anim.save(path, writer=writer)#, dpi=self.dpi)

        plt.close()

if __name__ == "__main__":
    body_data = [
        [(4, 1), (3, 1), (2, 1)], 
        [(4, 2), (4, 1), (3, 1)],
        [(4, 3), (4, 2), (4, 1)],
        [(4, 4), (4, 3), (4, 2)],
        [(5, 4), (4, 4), (4, 3)],
        [(6, 4), (5, 4), (4, 4)]
    ]

    food_data = [(4, 4), (4, 4), (4, 4), (7, 7), (7, 7), (7, 7)]

    animator = Animator(body_data=body_data, food_data=food_data)
    animator.make_animation()
