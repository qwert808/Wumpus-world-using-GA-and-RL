# environment.py
import random

def create_environment(grid_size, pit_prob=0.2):
    """Generate random Wumpus World with safe agent start."""
    environment = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place Wumpus and Gold
    wumpus_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    environment[wumpus_pos[0]][wumpus_pos[1]] = "W"
    
    gold_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    while gold_pos == wumpus_pos:
        gold_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    environment[gold_pos[0]][gold_pos[1]] = "G"
    
    # Place Pits
    for i in range(grid_size):
        for j in range(grid_size):
            if (i,j) not in [wumpus_pos, gold_pos] and random.random() < pit_prob:
                environment[i][j] = "P"
    
    # Place Agent safely
    agent_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    while environment[agent_pos[0]][agent_pos[1]] != "":
        agent_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    
    environment[agent_pos[0]][agent_pos[1]] = "A"
    return environment, agent_pos, wumpus_pos, gold_pos