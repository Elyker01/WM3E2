import random
from agents import Agent, Environment
import tkinter as tk

class SchellingAgent(Agent):
    def __init__(self, color, location):
        super().__init__(program=None)
        self.color = color
        self.location = location
        self.happy = False

    def check_happiness(self, world):
        similar = 0
        total = 0

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx, ny = self.location[0] + dx, self.location[1] + dy
                if 0 <= nx < world.width and 0 <= ny < world.height:
                    cell = world.grid[nx][ny]
                    if cell is not None and cell.color == self.color:
                        similar += 1
                    total += 1

        self.happy = similar >= 2

    def move(self, new_location):
        self.location = new_location

class SchellingWorld(Environment):
    def __init__(self, width=10, height=10):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.agents = []
        self.empty_cells = [(x, y) for x in range(width) for y in range(height)]

    def populate(self, n_agents, colors=('red', 'blue')):
        for _ in range(n_agents):
            color = random.choice(colors)
            location = random.choice(self.empty_cells)
            self.empty_cells.remove(location)
            agent = SchellingAgent(color, location)
            self.grid[location[0]][location[1]] = agent
            self.agents.append(agent)

    def draw(self):
        cell_size = 50  # size of each cell in pixels
        root = tk.Tk()
        canvas = tk.Canvas(root, width=self.width*cell_size, height=self.height*cell_size)
        canvas.pack()

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = 'white' if cell is None else cell.color
                canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)

        root.mainloop()

    def run(self, nSteps):
        for _ in range(nSteps):
            agent = random.choice(self.agents)
            agent.check_happiness(self)
            if not agent.happy:
                new_location = random.choice(self.empty_cells)
                self.empty_cells.remove(new_location)
                self.empty_cells.append(agent.location)
                self.grid[agent.location[0]][agent.location[1]] = None
                self.grid[new_location[0]][new_location[1]] = agent
                agent.move(new_location)
        self.draw()  # draw the final state of the world

# Create a new world
world = SchellingWorld(width=10, height=10)

# Populate the world with 90 agents (since 10% of the 100 cells should be empty)
world.populate(n_agents=90)

# Run the simulation for 100 steps
world.run(nSteps=100)