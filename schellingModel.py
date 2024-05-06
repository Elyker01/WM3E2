import random
import tkinter as tk

class Agent:
    def __init__(self, location):
        self.location = location

class SchellingAgent(Agent):
    def __init__(self, color, location=None):
        super().__init__(location)
        self.color = color
        self.happy = False
        self.neighbours = []

    def check_happiness(self):
        similar_neighbours = [n for n in self.neighbours if n.color == self.color]
        self.happy = len(similar_neighbours) >= 2

    def move(self, new_location):
        self.location = new_location

class SchellingWorld:
    def __init__(self, width=10, height=10):
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
        root = tk.Tk()
        canvas = tk.Canvas(root, width=self.width*10, height=self.height*10)
        canvas.pack()

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = 'white' if cell is None else cell.color
                canvas.create_rectangle(j*10, i*10, (j+1)*10, (i+1)*10, fill=color)

        root.mainloop()

    def run(self, nSteps):
        for _ in range(nSteps):
            agent = random.choice(self.agents)
            agent.check_happiness()
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