import numpy as np

NORTH = np.array([0, -1])
EAST = np.array([1, 0])
SOUTH = np.array([0, 1])
WEST = np.array([-1, 0])

class directions():

    def __init__(self):

        self.NORTH = np.array([0, -1])
        self.EAST = np.array([1, 0])
        self.SOUTH = np.array([0, 1])
        self.WEST = np.array([-1, 0])        


from agent_game.model import Linear_QNet, QTrainer

from agent_game.game_logic import Game, cell_count


class BasicAgent():

    def __init__(self, NN_layers, LR: float, gamma: float):
        self.control_type = "relative"
        self.NN_layers = NN_layers
        self.LR = LR
        self.gamma = gamma

    def get_model(self) -> Linear_QNet:
        return Linear_QNet(11, self.NN_layers, 3)
    
    def get_target_model(self, model: Linear_QNet) -> Linear_QNet:
        target_model = Linear_QNet(11, self.NN_layers, 3)
        target_model.load_state_dict(model.state_dict())
        target_model.eval()

        return target_model
    
    def get_trainer(self, model, target_model) -> QTrainer:
        return QTrainer(model=model, target_model=target_model, lr=self.LR, gamma=self.gamma)

    def get_state(self, game: Game):
        head = game.snake.body[0]
        point_n = head + NORTH
        point_e = head + EAST
        point_s = head + SOUTH
        point_w = head + WEST

        dir_n = (game.snake.direction == NORTH).all()
        dir_e = (game.snake.direction == EAST).all()
        dir_s = (game.snake.direction == SOUTH).all()
        dir_w = (game.snake.direction == WEST).all()


        state = [
            # Danger left
            (dir_n and game.CheckDanger(point_w)) or
            (dir_e and game.CheckDanger(point_n)) or
            (dir_s and game.CheckDanger(point_e)) or
            (dir_w and game.CheckDanger(point_s)),

            # Danger straight
            (dir_n and game.CheckDanger(point_n)) or
            (dir_e and game.CheckDanger(point_e)) or
            (dir_s and game.CheckDanger(point_s)) or
            (dir_w and game.CheckDanger(point_w)),

            # Danger right
            (dir_n and game.CheckDanger(point_e)) or
            (dir_e and game.CheckDanger(point_s)) or
            (dir_s and game.CheckDanger(point_w)) or
            (dir_w and game.CheckDanger(point_n)),

            # Move directions, only one is true
            dir_n,
            dir_e,
            dir_s,
            dir_w,

            game.food.position[0] < game.snake.head[0], # Food west
            game.food.position[0] > game.snake.head[0], # Food east
            game.food.position[1] < game.snake.head[1], # Food north
            game.food.position[1] > game.snake.head[1], # Food south

        ]

        return np.array(state, dtype=int)

class EgoAgent():

    def __init__(self, NN_layers, occupance_size, LR, gamma):

        self.control_type = "relative"

        self.NN_layers = NN_layers
        self.occupance_size = occupance_size 
        self.LR = LR
        self.gamma = gamma

    def get_model(self) -> Linear_QNet:
        return Linear_QNet(self.occupance_size**2 + 2, self.NN_layers, 3)
    
    def get_target_model(self, model: Linear_QNet) -> Linear_QNet:
        target_model = Linear_QNet(self.occupance_size**2 + 2, self.NN_layers, 3)
        target_model.load_state_dict(model.state_dict())
        target_model.eval()

        return target_model
    
    def get_trainer(self, model, target_model) -> QTrainer:
        return QTrainer(model=model, target_model=target_model, lr=self.LR, gamma=self.gamma)            

    def ego_occupance_grid(self, game, size=5, cell_count=20):
        local_coords = [(dx, dy) for dy in range(-(size//2),size//2+1) for dx in range(-(size//2),size//2+1)]
        
        grid = np.zeros((size,size), dtype=int)
        
        for i, (dx, dy) in enumerate(local_coords):
            head = game.snake.body[0]
            x, y = head[0] + dx, head[1] + dy
            
            # wall
            if x < 0 or x >= cell_count or y < 0 or y >= cell_count:
                grid[i//size, i%size] = 1
                continue
            
            # snake body
            for part in game.snake.body:
                if x == part[0] and y == part[1]:
                    grid[i//size, i%size] = 2
                    break
        
            if game.food.position[0] == x and game.food.position[1] == y:
                grid[i//size, i%size] = -1
        # rotate
        rot_map = {
            (0,-1): 0,
            (1,0): 1,
            (0,1): 2,
            (-1,0): -1,
        }
        k = rot_map[tuple(game.snake.direction)]
        grid = np.rot90(grid, k)
        
        return grid

    def get_state(self, game: Game):
        head = game.snake.body[0]
        point_n = head + NORTH
        point_e = head + EAST
        point_s = head + SOUTH
        point_w = head + WEST

        
        dir_n = (game.snake.direction == NORTH).all()
        dir_e = (game.snake.direction == EAST).all()
        dir_s = (game.snake.direction == SOUTH).all()
        dir_w = (game.snake.direction == WEST).all()
        

        food_x = game.food.position[0]
        food_y = game.food.position[1]

        head_x = head[0]
        head_y = head[1]

        food_is_north = food_y < head_y
        food_is_east = food_x > head_x

        """
        dirs = directions()

        match game.snake.direction:
            case dirs.NORTH:
                food_forward = food_is_north
                food_left = not food_is_east
            case dirs.EAST:
                food_forward = food_is_east
                food_left = not food_is_north
            case dirs.SOUTH:
                food_forward = not food_is_north
                food_left = food_is_east
            case dirs.WEST:
                food_forward = not food_is_east
                food_left = food_is_north

        """
        if dir_n:
            food_forward = food_is_north
            food_left = not food_is_east
        if dir_e:
            food_forward = food_is_east
            food_left = not food_is_north
        if dir_s:
            food_forward = not food_is_north
            food_left = food_is_east
        if dir_w:
            food_forward = not food_is_east
            food_left = food_is_north
        

        occupance_grid = self.ego_occupance_grid(game, size=self.occupance_size, cell_count=cell_count)

        state = np.concatenate((occupance_grid.flatten(), np.array([food_forward, food_left])))


        return state


if __name__ == "__main__":
    basic_agent = BasicAgent([128, 64, 64, 32], LR=0.001, gamma=0.9)

    print(basic_agent.model.parameters) 