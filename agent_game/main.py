"""
Main file to run RL snake simulations
"""
from agent_game.config.UI.main_window import run_main_window
from agent_game.config.UI.save_window import run_save_window

config_dir = "agent_game/config/config_files"
run_sim, active_profile, config = run_main_window(config_dir)

import pygame
from agent_game.agent import Agent
from agent_game.game_logic import Game
from agent_game.plotter import TrainingPlotter
from agent_game.video_generator import Animator

import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

agent_type = config.agent_type
NN_layers = [layer for layer in config.nn_layers if layer != 0]
occupance_size = config.occupance_size

MAX_MEMORY = config.max_memory
BATCH_SIZE = config.batch_size
LR = config.lr
gamma = config.gamma

timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M")

save_dir = agent_type + "_" + timestamp
save_path = os.path.join("agent_game", "results", save_dir)


def save_model_data(save_path, config, record, n_games):
    path = os.path.join(save_path, "model_data.json")
    model_data = config.__dict__
    model_data["record"] = record
    model_data["n_games"] = n_games
    with open(path, "w") as f:
        json.dump(model_data, f, indent=4)

def train():

    plot_scores = []
    plot_mean_scores = []
    plotter = TrainingPlotter()

    total_score = 0
    mean_window = 100
    record = 0

    target_model_interval = 10

    agent = Agent.from_type(agent_type=agent_type,
                            NN_layers=NN_layers,
                            occupance_size=occupance_size,
                            LR=LR,
                            gamma=gamma,
                            BATCH_SIZE=BATCH_SIZE,
                            MAX_MEMORY=MAX_MEMORY)


    game = Game(control_type=agent.net.control_type)    

    while True:

        step_triggered = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plt.close()
                pygame.quit()
                return game, record, agent

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # When Space is pressed, trigger one single step
                    step_triggered = True

        #if not step_triggered:
        #    continue

        # Get old state
        state_old = agent.get_state(game)
        # Get move
        final_action = agent.get_action(state_old)

        # Perform move and get new state
        reward, done, score = game.Step(final_action)


        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_action, reward, state_new, done)


        # Remember
        agent.remember(state_old, final_action, reward, state_new, done)


        if done:

            if agent.n_games % target_model_interval:
                agent.target_model.load_state_dict(agent.model.state_dict())

            # Train long memory
            game.Reset()
            agent.n_games += 1
            loss = agent.train_long_memory()

            if score > record:
                record = score
            
            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            if agent.n_games < mean_window:
                mean_score = total_score / agent.n_games
            else:
                mean_score = sum(plot_scores[-mean_window::])/mean_window

            plot_mean_scores.append(mean_score)
            plotter.update(plot_scores, plot_mean_scores)

    return game, record, agent


if run_sim:
    game, record, agent = train()

    save_info, save_weights, save_anim = run_save_window()

    if save_info or save_weights or save_anim:
        os.makedirs(save_path, exist_ok=False)

    # Save simulation info at end of training
    if save_info:
        n_games = agent.n_games
        save_model_data(save_path=save_path, config=config, record=record, n_games=n_games)

    # Save network parameters at end of training
    if save_weights:
        agent.model.save(save_path=save_path)

    # Save animation of BEST run
    if save_anim:
        animator = Animator(game.best_body_data, game.best_food_data)
        animator.make_animation(save_path=save_path)

    