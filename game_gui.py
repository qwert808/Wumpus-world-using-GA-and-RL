# game_gui.py
import tkinter as tk
from PIL import ImageGrab

class WumpusGUI:
    def __init__(self, root, grid_size):
        self.root = root
        self.grid_size = grid_size
        self.cell_size = 100
        self.canvas = tk.Canvas(root, width=grid_size*self.cell_size, 
                               height=grid_size*self.cell_size)
        self.canvas.pack()
        self.frames = []
        self.paused = False

    def draw_grid(self, environment, agent_pos=None):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                
                cell = environment[i][j]
                if cell == "W":
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="W", fill="red", font=("Arial", 24))
                elif cell == "P":
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="P", fill="blue", font=("Arial", 24))
                elif cell == "G":
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="G", fill="gold", font=("Arial", 24))
                elif cell == "A":
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="A", fill="green", font=("Arial", 24))
        
        self.capture_frame()

    def capture_frame(self):
        """Save current state for GIF."""
        self.canvas.update()
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        self.frames.append(ImageGrab.grab(bbox=(x, y, x1, y1)))

    def save_gif(self, filename="wumpus.gif"):
        if len(self.frames) > 1:
            self.frames[0].save(filename, save_all=True, 
                               append_images=self.frames[1:], 
                               duration=500, loop=0)
        self.frames = []

    def toggle_pause(self):
        self.paused = not self.paused