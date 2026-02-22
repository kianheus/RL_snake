# **RL-snake**
 Reinforcement Learning an agent to play the classic snake game in Python


## How it's made
<img src="demo_animation_(basic_46).gif" align="right" width="30%" />

**Tech used:** Python, PyTorch, PyQt6


I have developed a Python framework to configure, train and visualize reinforcement learning agents to play the classic Snake game. The agent plays on a 20x20 grid of open squares, and its goal is to collect as many "apples" as possible. Each apple eaten increases the snake's length. I used a Deep Q-Learning (DQN) approach to this problem, because it is beginner-friendly and good documentation exists online. To make the selection of agent type and hyperparameters more user-friendly, I created a PyQt6 UI. Details of this interface are provided in the "Build and run" section below.

<br>

I created 3 state possible state representations, which are listed as separate "agent architectures". These are:

1. **Basic agent:** This state representation TODO: Fill in
2. **Ego agent:** This representation contains a square grid around the snake head, with each point listed as either free space, wall, body part or food. Furthermore, the food direction relative to the head is added for cases when the food is further away. TODO: Something about this representation and convolution?
3. **RayCast agent:** This state representation is inspired by existing RL-projects [^link??], and features 8 "rays" which point from the snake head. Each ray gives information about the distance to walls, and the distance to body parts. Furthermore, the food direction is added to the state. This is conceptually similar to the basic agent, but provides a less near-sighted state.




[^1]



## Results
All three agent architectures are able to learn an effective basic strategy to gather food and avoid immediate danger. The basic agent averages at a score of around 25, with a high score of around 60 (after 1000 games). The ego agent performs slightly better, averaging 30 with a similar high score of around 60. The raycast agent with a larger neural network significantly outperformed the other agent architectures, averaging a score above 40, with a high score of 80. 

The most obvious shortcoming of this reinforcement learning approach is that the agents do not seem to learn high-level strategy. They most frequently lose because they trap themselves, leaving no possible escape. This is expected for the basic agent, due to its myopic state representation. In principle, however, the other agents should have rich enough features to learn strategy. It is possible that the reward function too harshly prioritizes immediate reward, forcing the agent to take decisions that limit long-term survivability.

It is difficult for me to say whether the limited results of this RL approach are due to implementation mistakes, or if this is inherent to the chosen method. 

## Build and run
For installation, I assume that you have Python version 3.12 and conda installed. Python downloads can be found [<u>here</u>](https://www.python.org/downloads/), and a conda installation tutorial is provided [<u>here</u>](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

To install this project, clone this repository in your desired directory using:

```
git clone https://github.com/kianheus/RL_snake.git
```

Then move to the directory and install the dependencies using conda:

```
cd RL_snake
conda env create -f environment.yml
```

This creates a virtual environment with the required python packages. The installed version of PyTorch runs on CPU, which is not as performant as running on GPU. For GPU-compatible installation instructions, see [<u>here</u>](https://pytorch.org/get-started/locally/).


### Running the code
To run the code, activate the environment and run the main file:
```
conda activate RL_snake
python -m agent_game.main
```

You will be prompted with a UI to select and create an agent profile, and choose hyperparameters. Once you have set up your simulation as desired, press "save and run" to run the simulation. After closing the PyGame simulation window, you will be prompted to save information about the training. Choose the options you want, and save, or close to abort. 
## Lessons learned


Things I want to talk about:






[^1] Hello