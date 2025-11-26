import torch
import time
import random
import numpy as np
from collections import deque
import warnings
warnings.filterwarnings("ignore", module="pygame")

from game_logic import Game
from conv_model import CNN_QNet, QTrainer
from plotter import plot


MAX_MEMORY = 100_000
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
        self.model = CNN_QNet(20, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def Get_State(self, game: Game, N=20):

        state = np.zeros((6, N, N), dtype = np.float32)

        for cell in game.snake.body:
            state[0, cell[0], cell[1]] = 1

        fx, fy = game.food.position[0], game.food.position[1]
        state[1, fy, fx] = 1


        hx, hy = game.snake.head[0], game.snake.head[1]

        if (game.snake.direction == NORTH).all():
            state[2, hy, hx] = 1
        if (game.snake.direction == EAST).all():
            state[3, hy, hx] = 1
        if (game.snake.direction == SOUTH).all():
            state[4, hy, hx] = 1
        if (game.snake.direction == WEST).all():
            state[5, hy, hx] = 1

        return torch.tensor(state)#.unsqueeze(0)
        

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # Pops left if max memory is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        states = np.stack(states, axis=0)
        next_states = np.stack(next_states, axis=0)
        actions = np.stack(actions, axis=0)

        states = torch.tensor(states, dtype=torch.float)#.squeeze(0)
        next_states = torch.tensor(next_states, dtype=torch.float)#.squeeze(0)
        actions = torch.tensor(actions, dtype=torch.float)#.squeeze(0)

        print("LONG: states.shape:", states.shape)

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


    t_state_old = 0
    t_final_action = 0
    t_rewarddonescore = 0
    t_state_new = 0
    t_train_short_memory = 0
    t_remember = 0
    t_train_long_memory = 0
    t_plotting = 0

    while True:

        timer_state_old = time.time()
        # Get old state
        state_old = agent.Get_State(game)
        t_state_old += time.time() - timer_state_old

        # Get move
        timer_final_action = time.time()
        final_action = agent.get_action(state_old)
        t_final_action += time.time() - timer_final_action

        # Perform move and get new state
        timer_rewarddonescore = time.time()
        reward, done, score = game.Step(final_action)
        t_rewarddonescore += time.time() - timer_rewarddonescore

        timer_state_new = time.time()
        state_new = agent.Get_State(game)
        t_state_new += time.time() - timer_state_new

        # Train short memory
        timer_train_short_memory = time.time()
        agent.train_short_memory(state_old, final_action, reward, state_new, done)
        t_train_short_memory += time.time() - timer_train_short_memory

        # Remember
        timer_remember = time.time()
        agent.remember(state_old, final_action, reward, state_new, done)
        t_remember += time.time() - timer_remember


        if done:
            # Train long memory
            game.Reset()
            agent.n_games += 1

            timer_train_long_memory = time.time()
            agent.train_long_memory()
            t_train_long_memory += time.time() - timer_train_long_memory
            print("Memory size:", len(agent.memory))

            if score > record:
                record = score
                agent.model.save()
            
            print("Game", agent.n_games, "Score", score, "Record:", record)


            timer_plotting = time.time()
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            t_plotting += time.time() - timer_plotting


            print("t_state_old", t_state_old)
            print("t_final_action", t_final_action)
            print("t_rewarddonescore", t_rewarddonescore)
            print("t_state_new", t_state_new)
            print("t_train_short_memory", t_train_short_memory)
            print("t_remember", t_remember)
            print("t_train_long_memory", t_train_long_memory)
            print("t_plotting", t_plotting)            

        if agent.n_games >= 80:
            time.sleep(0.05)

if __name__ == "__main__":


    train()