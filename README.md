# Snake Game with Reinforcement Learning

## Overview

The game consists of two snakes:
1. **Player Snake (Green)**: Controlled by the player using keyboard inputs.
2. **AI Snake (Blue)**: Controlled by an AI agent using reinforcement learning.

Both snakes aim to eat the red rat that appears randomly on the board. Each time a snake eats a rat, it grows in length and earns a point. The game ends when a snake collides with the wall, itself, or the other snake. The first snake to reach a specified number of points wins the game.

## Features

- Human vs. AI gameplay.
- AI-controlled snake using reinforcement learning (Q-learning with a neural network).
- Dynamic game speed based on the current level.
- Ability to pause, reset, save, and load game states.
- Real-time statistics to monitor AI training progress.

## How to Play

### Controls
- **Arrow Keys**: Control the player's snake.
- **Buttons**: Control the game state (Start, Reset, Save State, Load State, Exit, Pause, Statistics).

### Buttons
- **Start**: Starts the game.
- **Reset**: Resets the game to its initial state.
- **Save State**: Saves the current game state.
- **Load State**: Loads a previously saved game state.
- **Exit**: Exits the game.
- **Pause**: Pauses the game.
- **Statistics**: Displays real-time training statistics of the AI snake.

## Statistics Function

The statistics function provides real-time insights into the AI snake's training progress. It helps players and developers understand how the AI is learning and improving over time. The statistics are displayed using matplotlib and include the following plots:

1. **Training Loss**: Displays the loss value of the AI's neural network over episodes, showing how the model's accuracy improves.
2. **Reward History**: Shows the rewards earned by the AI snake over episodes, indicating the success rate of the AI's actions.
3. **Moving Average of Reward**: Plots the moving average of rewards over a window of 50 episodes, providing a smoothed view of the AI's performance trend.
4. **Exploration Rate**: Displays the exploration rate over time, showing how the AI gradually shifts from exploration to exploitation as it learns.
5. **Cumulative Rewards**: Shows the cumulative rewards earned by the AI snake, indicating its overall progress.
6. **Predicted Performance**: Plots the predicted performance of the AI over a window of 100 episodes and highlights the best performance achieved.

### How It Helps

The statistics function helps in the following ways:
- **Performance Monitoring**: By observing the training loss and reward history, players can see how well the AI is learning and adapting to the game.
- **Trend Analysis**: The moving average of rewards provides a clearer view of the AI's performance trends, helping to identify periods of improvement or decline.
- **Exploration vs. Exploitation**: The exploration rate plot shows how the AI balances exploration (trying new actions) and exploitation (choosing the best-known actions), which is crucial for effective learning.
- **Progress Tracking**: The cumulative rewards plot gives an overall sense of the AI's progress and success in the game.

## A GLIMPSE

![Snake Game Screenshot](Screenshots/Screenshot_3.png)  

## Features

- **Player Snake**: Controlled by the user with the arrow keys.
- **AI Snake**: Controlled by a reinforcement learning agent using DQN.
- **Rats**: The goal is to eat the rats that appear on the board.
- **Levels and Matches**: Progress through levels and matches by eating rats and avoiding collisions.
- **Save and Load**: Save the game state and AI model to continue later.
- **Statistics**: Real-time statistics of the AI's training process.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/SnakeGameRL.git
    cd SnakeGameRL
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the game**:
    ```bash
    python main.py
    ```

## Reinforcement Learning Methods

The AI snake in this game uses a Deep Q-Network (DQN) to learn from its actions. Here’s a brief explanation of the method:

### Deep Q-Network (DQN)

1. **State Representation**: The game board is represented as a grid, where the position of the player snake, AI snake, and rats are encoded as states.
2. **Action Space**: The possible actions (UP, DOWN, LEFT, RIGHT) that the snake can take.
3. **Q-Function**: A neural network is used to approximate the Q-function, which predicts the expected future rewards for each action given a state.
4. **Experience Replay**: The agent stores its experiences (state, action, reward, next state) in a memory buffer and samples from it to update the Q-network, which helps to break the correlation between consecutive experiences.
5. **Exploration vs. Exploitation**: The agent uses an ε-greedy policy to balance exploration (trying new actions) and exploitation (using actions that are known to yield high rewards).

### How It Helps in Studying Reinforcement Learning

- **Interactive Learning**: Playing against an AI that learns and improves provides an interactive way to see reinforcement learning in action.
- **Real-Time Training**: The game includes real-time statistics to visualize the training process of the AI.
- **Customizable**: The code is modular and can be modified to experiment with different reinforcement learning algorithms and strategies.

## Future Work

- **Game World Segmentation**: Pre-segmenting the game world to simplify state representation and improve the AI's learning efficiency.
- **Advanced AI Techniques**: Implementing more advanced techniques like Double DQN, Dueling DQN, or Proximal Policy Optimization (PPO).
- **Enhanced Graphics and UI**: Improving the game’s visual appeal and user interface for a better gaming experience.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Pygame for the game framework.
- Keras and TensorFlow for the deep learning libraries.
- The Pygame and Reinforcement Learning communities for their tutorials and support.
