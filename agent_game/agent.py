import torch
import pygame
import time
import random
import numpy as np
from collections import deque
import warnings
warnings.filterwarnings("ignore", module="pygame")

from game_logic import Game 
from model import Linear_QNet, QTrainer
from plotter import plot


MAX_MEMORY = 10000
BATCH_SIZE = 1000
LR = 0.001

NORTH = np.array([0, 1])
EAST = np.array([1, 0])
SOUTH = np.array([0, -1])
WEST = np.array([-1, 0])

class Agent():

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9 # Discount rate (<1)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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
        

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # Pops left if max memory is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model.forward(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


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
            agent.train_long_memory()
            print("Memory size:", len(agent.memory))

            if score > record:
                record = score
                agent.model.save()
            
            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

        if agent.n_games >= 80:
            time.sleep(0.05)

if __name__ == "__main__":
    train()