import numpy as np


def check_reachable(grid: np.ndarray) -> bool:

    free_space_x, free_space_y = (grid == 0).nonzero()

    # Keep track of all connected free points
    visited = set()

    # Take starting entry
    queue = [(free_space_x[0], free_space_y[0])]

    # Offsets to check for neighbouring indices
    offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    
    # Iteratively check neighbours of entry in connected set
    while queue:

        # Get current entry
        x, y = queue.pop()
        visited.add((x, y))

        for dx, dy in offsets:
                
                #Generate all neighbours of the newest point
                n_x = x + dx
                n_y = y + dy

                #Check if indices are valid (prevent wraparound or indexing too far)
                if n_x >= 0 and n_x < grid.shape[0] and n_y >= 0 and n_y < grid.shape[1]:

                    # Check if neighbour is free space
                    if grid[n_x, n_y] == 0 and (n_x, n_y) not in visited:
                        queue.append((n_x, n_y))


    if len(visited) == len(free_space_x):
         return True
    else:
         return False
    
if __name__ == "__main__":
        
    grid_open = np.array([[0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [1, 1, 0, 0],
                        [0, 0, 0, 0]])

    grid_closed = np.array([[0, 0, 0, 0],
                            [0, 1, 1, 0],
                            [1, 0, 1, 0],
                            [1, 1, 1, 0]])
    grid_open_reachable = check_reachable(grid_open)
    grid_closed_reachable = check_reachable(grid_closed)

    print("grid_open reachable:", grid_open_reachable)
    print("grid_closed reachable:", grid_closed_reachable)
