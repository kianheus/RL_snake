import torch
import pygame
import numpy as np
import random
import warnings
from collections import deque

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#warnings.filterwarnings("ignore")

import agent_game.agent_architectures as agent_architectures
from agent_game.game_logic import Game
from agent_game.config.agent_config import AgentType


class Agent():

    def __init__(self, net, BATCH_SIZE, MAX_MEMORY):
        self.net = net
        self.BATCH_SIZE = BATCH_SIZE
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = self.net.get_model()
        self.target_model = self.net.get_target_model(self.model)
        self.trainer = self.net.get_trainer(self.model, self.target_model)

        self.n_games = 0
        self.epsilon = 0


    def get_state(self, game:Game):
        state = self.net.get_state(game)
        return state
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > self.BATCH_SIZE:
            mini_sample = random.sample(self.memory, self.BATCH_SIZE) # List of tuples
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

    def get_action(self, state, train_len = 500):
        self.epsilon = train_len - self.n_games
        final_move = [0] * self.net.n_outputs
        if random.randint(0, train_len*2) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float, device=device)
            prediction = self.model.forward(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

    @staticmethod
    def from_type(agent_type: str, **kwargs):

        BATCH_SIZE = kwargs.get("BATCH_SIZE")
        MAX_MEMORY = kwargs.get("MAX_MEMORY")

        if agent_type == AgentType.BASIC:
            net = agent_architectures.BasicAgent(NN_layers=kwargs["NN_layers"], 
                                                 LR=kwargs["LR"],
                                                 gamma=kwargs["gamma"])
        elif agent_type == AgentType.EGO:
            net = agent_architectures.EgoAgent(NN_layers=kwargs["NN_layers"],
                                               occupance_size=kwargs["occupance_size"],
                                               LR=kwargs["LR"],
                                               gamma=kwargs["gamma"])
        elif agent_type == AgentType.RAYCAST:
            net = agent_architectures.RayCastAgent(NN_layers=kwargs["NN_layers"],
                                                   LR=kwargs["LR"],
                                                   gamma=kwargs["gamma"])
        else:
            raise ValueError(f"Unknown agent type {agent_type}")

        return Agent(net, BATCH_SIZE=BATCH_SIZE, MAX_MEMORY=MAX_MEMORY)

if __name__ == "__main__":

    agent = Agent.from_type("ego",
                            NN_layers=[128, 64, 32],
                            occupance_size=7,
                            LR=0.001,
                            gamma=0.9)

    print(agent.net)