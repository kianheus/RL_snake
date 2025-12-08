"""
Main file to run RL snake simulations
"""

import pygame

from agent_game.agent_constructor import Agent
from game_logic import Game
from plotter import plot

MAX_MEMORY = 10000
BATCH_SIZE = 1000
LR = 0.001
gamma = 0.9

#TODO: Make an interactive display to choose parameters for different types of agents

agent_type = "ego" # Choose from "ego", "basic", "conv"
NN_layers = [128, 64, 64] # Size of hidden layers (fully connected with ReLU activation)





### If you are using an ego-agent, change these variables:
occupance_size = 7


agent = Agent.from_type("ego",
                        NN_layers=NN_layers,
                        occupance_size=occupance_size,
                        LR=LR,
                        gamma=gamma,
                        BATCH_SIZE=BATCH_SIZE,
                        MAX_MEMORY=MAX_MEMORY)


game = Game(control_type=agent.net.control_type)


def train():

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    mean_window = 100
    record = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return record

        # Get old state
        state_old = agent.get_state(game)
        # Get move
        final_action = agent.get_action(state_old)

        if agent.n_games % 10 == 0:
            agent.target_model.load_state_dict(agent.model.state_dict())


        # Perform move and get new state
        reward, done, score = game.Step(final_action)


        state_new = agent.get_state(game)

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
            
            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            if agent.n_games < mean_window:
                mean_score = total_score / agent.n_games
            else:
                mean_score = sum(plot_scores[-mean_window::])/mean_window

            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

record = train()

print(record)