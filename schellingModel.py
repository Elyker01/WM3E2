import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class SchellingModel:
    def __init__(self, grid_size, red_ratio, blue_ratio):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))  # Initialize grid with empty cells
        self.populate_grid(red_ratio, blue_ratio)
    
    def populate_grid(self, red_ratio, blue_ratio):
        total_cells = self.grid_size * self.grid_size
        num_red = int(red_ratio * total_cells)
        num_blue = int(blue_ratio * total_cells)
        agent_positions = random.sample(range(total_cells), num_red + num_blue)
        for pos in agent_positions[:num_red]:
            x, y = divmod(pos, self.grid_size)
            self.grid[x, y] = 1  # Red agent
        for pos in agent_positions[num_red:]:
            x, y = divmod(pos, self.grid_size)
            self.grid[x, y] = 2  # Blue agent
    
    def check_neighborhood(self, x, y):
        similar_neighbors = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                    if self.grid[new_x, new_y] == self.grid[x, y]:
                        similar_neighbors += 1
        return similar_neighbors
    
    def is_happy(self, x, y):
        similar_neighbors = self.check_neighborhood(x, y)
        total_neighbors = 8  # Eight cells in the neighborhood
        threshold = 0.5  # Threshold for similarity (50%)
        return similar_neighbors >= total_neighbors * threshold
    
    def move_unhappy_agent(self, x, y):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i, j] == 0]
        similar_fractions = []
        for empty_x, empty_y in empty_cells:
            similar_neighbors = self.check_neighborhood(empty_x, empty_y)
            total_neighbors = 8  # Eight cells in the neighborhood
            if total_neighbors == 0:
                similar_fraction = 0
            else:
                similar_fraction = similar_neighbors / total_neighbors
            similar_fractions.append(similar_fraction)
        best_empty_cell = empty_cells[np.argmax(similar_fractions)]
        self.grid[best_empty_cell[0], best_empty_cell[1]] = self.grid[x, y]
        self.grid[x, y] = 0
    
    def simulate(self, num_steps):
        for _ in range(num_steps):
            unhappy_agents = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i, j] != 0 and not self.is_happy(i, j)]
            if len(unhappy_agents) == 0:
                print("All agents are happy. Simulation terminated.")
                break
            x, y = random.choice(unhappy_agents)
            self.move_unhappy_agent(x, y)
    
    def visualize(self):
        cmap = ListedColormap(['white', 'red', 'blue'])
        plt.matshow(self.grid, cmap=cmap)
        plt.title("Schelling Model of Segregation")
        plt.xlabel("Grid X")
        plt.ylabel("Grid Y")
        plt.show()

# Example usage
model = SchellingModel(grid_size=10, red_ratio=0.4, blue_ratio=0.4)
model.simulate(num_steps=100)
model.visualize()
