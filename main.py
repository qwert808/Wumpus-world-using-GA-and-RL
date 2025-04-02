# main.py (complete fixed version)
import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
from collections import defaultdict
from agent import perceive_environment, move_agent
from environment import create_environment
from game_gui import WumpusGUI

class WumpusGame:
    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.reset_environment()
        self.root = tk.Tk()
        self.gui = WumpusGUI(self.root, grid_size)
        self.setup_ui()

    def reset_environment(self):
        self.environment, self.agent_pos, self.wumpus_pos, self.gold_pos = create_environment(self.grid_size)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        tk.Button(control_frame, text="Start GA", command=self.run_ga).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Start RL", command=self.run_rl).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Pause", command=self.gui.toggle_pause).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT)

        self.gui.draw_grid(self.environment, self.agent_pos)

    def reset(self):
        self.reset_environment()
        self.gui.draw_grid(self.environment, self.agent_pos)

    # ========== RL METHODS ==========
    def get_reward(self, state):
        """Calculate reward for RL agent."""
        x, y = state
        if (x, y) == self.gold_pos:
            return 100
        elif self.environment[x][y] in ["W", "P"]:
            return -100
        elif "Stench" in perceive_environment(self.environment, state, self.grid_size):
            return -10
        else:
            return -1

    def choose_action(self, q_table, state, epsilon=0.1):
        """ε-greedy action selection."""
        if random.random() < epsilon:
            return random.randint(0, 3)  # Explore
        return np.argmax(q_table[state])  # Exploit

    def extract_path(self, q_table, max_steps=20):
        """Extract path from Q-table."""
        path = []
        state = self.agent_pos
        for _ in range(max_steps):
            action = np.argmax(q_table[state])
            move = ["up", "down", "left", "right"][action]
            path.append(move)
            state, _ = move_agent(self.environment.copy(), state, move, self.grid_size)
            if state == self.gold_pos:
                break
        return path

    # ========== GA METHODS ==========
    def fitness(self, path):
        """Evaluate path fitness."""
        score = 0
        current_pos = self.agent_pos
        env_copy = [row[:] for row in self.environment]
        
        for move in path:
            current_pos, status = move_agent(env_copy, current_pos, move, self.grid_size)
            if status == "failure":
                return -1000
            if current_pos == self.gold_pos:
                return 1000
            score -= 1  # Penalize longer paths
        return score

    def evolve_population(self, population, scores):
        """Genetic Algorithm operations."""
        # Selection (keep top 50%)
        sorted_pop = [x for _,x in sorted(zip(scores, population), reverse=True)]
        new_pop = sorted_pop[:len(population)//2]
        
        # Crossover and mutation
        while len(new_pop) < len(population):
            parent1, parent2 = random.choices(new_pop, k=2)
            split = random.randint(1, len(parent1)-1)
            child = parent1[:split] + parent2[split:]
            
            # Mutation
            if random.random() < 0.1:
                idx = random.randint(0, len(child)-1)
                child[idx] = random.choice(["up", "down", "left", "right"])
            new_pop.append(child)
        
        return new_pop

    # ========== EXECUTION ==========
    def run_rl(self):
        """Run Q-learning algorithm."""
        q_table = defaultdict(lambda: np.zeros(4))  # 4 actions
        
        # Training
        for _ in range(1000):
            state = self.agent_pos
            env_copy = [row[:] for row in self.environment]
            
            while True:
                action = self.choose_action(q_table, state)
                move = ["up", "down", "left", "right"][action]
                next_state, _ = move_agent(env_copy, state, move, self.grid_size)
                reward = self.get_reward(next_state)
                
                # Q-learning update
                best_next = np.max(q_table[next_state])
                q_table[state][action] += 0.1 * (reward + 0.9 * best_next - q_table[state][action])
                
                state = next_state
                if reward == 100 or reward == -100:  # Terminal state
                    break
        
        # Execute learned policy
        path = self.extract_path(q_table)
        self.execute_path(path)

    def run_ga(self):
        """Run Genetic Algorithm."""
        population = [[random.choice(["up", "down", "left", "right"]) for _ in range(10)] 
                     for _ in range(50)]
        
        for _ in range(100):
            scores = [self.fitness(path) for path in population]
            
            if max(scores) >= 1000:  # Found gold
                best_path = population[np.argmax(scores)]
                self.execute_path(best_path)
                return
            
            population = self.evolve_population(population, scores)
        
        # If no perfect solution, use best found
        best_path = population[np.argmax([self.fitness(p) for p in population])]
        self.execute_path(best_path)

    def execute_path(self, path):
        """Visualize path execution."""
        current_pos = self.agent_pos
        env_copy = [row[:] for row in self.environment]
        
        for move in path:
            current_pos, status = move_agent(env_copy, current_pos, move, self.grid_size)
            self.gui.draw_grid(env_copy, current_pos)
            self.root.update()
            
            if status == "failure":
                messagebox.showinfo("Game Over", "Agent died!")
                return
            if current_pos == self.gold_pos:
                messagebox.showinfo("Success", "Found gold!")
                self.gui.save_gif()
                return
            
            while self.gui.paused:
                self.root.update()
            self.root.after(500)  # Delay for visibility

if __name__ == "__main__":
    game = WumpusGame()
    game.root.mainloop()