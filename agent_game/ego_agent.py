import torch
import pygame
import time
import random
import numpy as np
from collections import deque
import warnings

from game_logic import Game
from agent_types import EgoAgent
from model import Linear_QNet, QTrainer
from plotter import plot
from game_logic import cell_count

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
warnings.filterwarnings("ignore", module="pygame")

MAX_MEMORY = 10000
BATCH_SIZE = 1000
LR = 0.001

NORTH = np.array([0, -1])
EAST = np.array([1, 0])
SOUTH = np.array([0, 1])
WEST = np.array([-1, 0])


class Agent():

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9 # Discount rate (<1)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.occupance_size = 7
        self.model = Linear_QNet(self.occupance_size**2 + 2, 32, 3)

        self.target_model = Linear_QNet(self.occupance_size**2 + 2, 32, 3)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()

        self.trainer = QTrainer(self.model, self.target_model, lr=LR, gamma=self.gamma)
        

    def Ego_Occupance_Grid(self, game, size=5, cell_count=20):
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

    def Get_State(self, game: Game):
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

        occupance_grid = self.Ego_Occupance_Grid(game, size=self.occupance_size, cell_count=cell_count)

        state = np.concatenate((occupance_grid.flatten(), np.array([food_forward, food_left])))


        return state
        

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        states      = np.array(states, dtype=np.float32)
        actions     = np.array(actions, dtype=np.float32)
        rewards     = np.array(rewards, dtype=np.float32)
        next_states = np.array(next_states, dtype=np.float32)
        dones       = np.array(dones, dtype=np.float32)

        loss = self.trainer.train_step(states, actions, rewards, next_states, dones)
        return loss

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, train_len = 100):
        self.epsilon = train_len - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, train_len*2) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float, device=device)
            prediction = self.model.forward(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    mean_window = 10
    record = 0
    agent = Agent()
    game = Game(control_type="relative")

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return record


        # Get old state
        state_old = agent.Get_State(game)
        # Get move
        final_action = agent.get_action(state_old)


        # Perform move and get new state
        reward, done, score = game.Step(final_action)


        state_new = agent.Get_State(game)

        # Train short memory
        agent.train_short_memory(state_old, final_action, reward, state_new, done)


        # Remember
        agent.remember(state_old, final_action, reward, state_new, done)


        if done:
            # Train long memory
            game.Reset()
            agent.n_games += 1
            loss = agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            

            plot_scores.append(score)
            total_score += score
            if agent.n_games < mean_window:
                mean_score = total_score / agent.n_games
            else:
                mean_score = sum(plot_scores[-mean_window::])/mean_window

            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

def manual():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    mean_window = 10
    record = 0
    agent = Agent()
    game = Game(control_type = "absolute")

    LEFT = [1, 0, 0]
    STRAIGHT = [0, 1, 0]
    RIGHT = [0, 0, 1]
    WindowShouldClose = False
    while not WindowShouldClose:

        wait_for_input = True

        while wait_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WindowShouldClose = True

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        WindowShouldClose = True
                        wait_for_input = False

                    if event.key == pygame.K_UP:
                        manual_action = NORTH
                        wait_for_input = False
                    if event.key == pygame.K_RIGHT:
                        manual_action = EAST
                        wait_for_input = False
                    if event.key == pygame.K_DOWN:
                        manual_action = SOUTH
                        wait_for_input = False
                    if event.key == pygame.K_LEFT:
                        manual_action = WEST
                        wait_for_input = False


        # Get old state
        state_old = agent.Get_State(game)

        # Perform move and get new state
        reward, done, score = game.Step(manual_action)


        state_new = agent.Get_State(game)

        # Train short memory
        agent.train_short_memory(state_old, manual_action, reward, state_new, done)


        # Remember
        agent.remember(state_old, manual_action, reward, state_new, done)



        if done:
            # Train long memory
            game.Reset()
            agent.n_games += 1
            agent.train_long_memory()
            print("Memory size:", len(agent.memory))

            if score > record:
                record = score
                agent.model.save()
            
            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            if agent.n_games < mean_window:
                mean_score = total_score / agent.n_games
            else:
                mean_score = sum(plot_scores[-mean_window::])/mean_window

            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    record = train()
    print("Done, saving record:", record)
    #manual()