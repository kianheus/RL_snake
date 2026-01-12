"""
Main file to run RL snake simulations
"""
from agent_game.config.UI.main_window import run_main_window

config_dir = "agent_game/config/config_files"
active_profile, config_data = run_main_window(config_dir)

import pygame
agent_type = config_data.agent_type
NN_layers = [layer for layer in config_data.nn_layers if layer != 0]
occupance_size = config_data.occupance_size

MAX_MEMORY = config_data.max_memory
BATCH_SIZE = config_data.batch_size
LR = config_data.lr
gamma = config_data.gamma





### If you are using an ego-agent, change these variables:
occupance_size = 7


from agent_game.agent_constructor import Agent
from agent_game.game_logic import Game
from agent_game.plotter import plot



def train():

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    mean_window = 100
    record = 0
    agent = Agent.from_type(agent_type=agent_type,
                            NN_layers=NN_layers,
                            occupance_size=occupance_size,
                            LR=LR,
                            gamma=gamma,
                            BATCH_SIZE=BATCH_SIZE,
                            MAX_MEMORY=MAX_MEMORY)


    game = Game(control_type=agent.net.control_type)    

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