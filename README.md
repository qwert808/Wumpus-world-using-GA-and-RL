# Wumpus World AI Game

## Overview
Wumpus World is a grid-based game where an AI agent navigates a hazardous environment to find gold while avoiding the Wumpus and pits. This implementation provides a GUI and integrates two AI approaches: **Genetic Algorithm (GA)** and **Reinforcement Learning (RL)** to solve the game.

## Features
- **Graphical User Interface (GUI):** Visual representation of the grid, agent movements, and hazards.
- **Genetic Algorithm (GA):** Evolves paths to find an optimal route to the gold.
- **Reinforcement Learning (RL):** Uses Q-learning to train the agent for optimal decision-making.
- **Game Controls:** Start/Pause/Reset buttons to manage the game execution.
- **Save as GIF:** The game records movements and can be saved as a GIF for analysis.

## Technologies Used
- **Python**
- **Tkinter** (for GUI)
- **NumPy** (for numerical operations)
- **Random** (for randomized moves and mutations)
- **Collections** (for handling Q-learning tables)

## Installation
Ensure you have Python installed, then install dependencies using:
```sh
pip install numpy
```

## Game Mechanics
### Grid Environment
- The environment consists of a **4x4 grid**.
- The agent starts in the bottom-left cell.
- The gold is placed randomly.
- Hazards:
  - **Wumpus:** If the agent moves here, it dies.
  - **Pits:** Falling into a pit results in failure.
  - **Stench & Breeze:** Indicate nearby dangers.

### AI Approaches
#### Reinforcement Learning (RL)
- Uses **Q-learning** to learn the best moves over **1000 episodes**.
- Rewards:
  - **+100** for reaching gold.
  - **-100** for encountering Wumpus or pit.
  - **-10** for sensing Wumpus.
  - **-1** per step to encourage shorter paths.
- Uses **ε-greedy strategy** for action selection.

#### Genetic Algorithm (GA)
- Evolves paths through **selection, crossover, and mutation**.
- Evaluates fitness based on:
  - Shorter paths (**higher fitness**).
  - Avoiding hazards.
  - Successfully reaching gold (**max fitness: 1000**).
- **Mutation rate:** 10% chance of random move mutation.

## Controls
- **Start GA:** Runs Genetic Algorithm.
- **Start RL:** Runs Reinforcement Learning.
- **Pause:** Temporarily stop execution.
- **Reset:** Resets the environment.

## Future Enhancements
- Implement **Deep Q-Learning (DQN)** for improved RL performance.
- Increase grid size for a more complex challenge.
- Add **multiple agents** with cooperative strategies.

## Author
**Dip Biswas**  
Email: [qwert.shan88@gmail.com]


## License
This project is open-source under the **MIT License**. Feel free to contribute and enhance the project!

