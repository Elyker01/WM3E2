import random
from time import *
import tkinter as tk
from collections import defaultdict
from agents import *

class SchellingModelAgent(Agent):
    def __init__(self, colour, location, k):
        super().__init__(program=self.agentProgram)
        self.colour = colour
        self.location = location
        self.happy = False
        self.k = k # Number of considered empty locations to move into

    def move(self, newLocation):

        # Move the agent to the new location
        self.location = newLocation      

    def agentProgram(self, percept):

        similarNeighbors = 0
        emptyNeighbors = 0
        
        # Iterate through the colours and locations and count the number of similar and empty neighbors
        for neighbor in percept:
            if neighbor['colour'] == self.colour:
                similarNeighbors += 1
            elif neighbor['colour'] == 'empty':
                emptyNeighbors += 1
        
        # If there are no empty neighbours then the agent action will be stay
        if emptyNeighbors == 0:
            return 'stay'
        
        # Calculate the fraction of similar neighbors
        totalNeighbors = len(percept) # Total number of neighbors
        if totalNeighbors > 0:
            similarFraction = similarNeighbors / totalNeighbors
        else:
            similarFraction = 0
        
        # If the fraction of similar neighbors is bigger than 0.25 then the agent action will be stay
        if similarFraction > 0.25:
            self.happy = True
            return 'stay'
        


class SchellingModelWorld(Environment):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        # Create a grid of size width * height which will be the world
        self.grid = []
        for rowIndex in range(width):
            row = []
            for columnIndex in range(height):
                row.append(None)
            self.grid.append(row)

        # Create an array of empty cells
        self.emptyCells = []
        for x in range(width):
            for y in range(height):
                self.emptyCells.append((x, y))

    def populate(self, nAgents, colours=('red', 'blue'), k=10):
        for _ in range(nAgents):
            # Choose a random colour and location for the agent and remove it from the empty cells array
            colour = random.choice(colours)
            location = random.choice(self.emptyCells)
            self.emptyCells.remove(location)

            # Create a new agent and add it to the grid and agent array from the environment class
            agent = SchellingModelAgent(colour, location, k)
            self.grid[location[0]][location[1]] = agent
            self.agents.append(agent)

    def draw(self):

        # Create the canvas to draw the world
        cellSize = 45 
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width*cellSize, height=self.height*cellSize)
        self.canvas.pack()
    
        for rowIndex, row in enumerate(self.grid): #Iterates through all cells in the grid
            for columnIndex, cell in enumerate(row):
                if cell is None: 
                    colour = 'white' #If the cell is empty, then the colour is white
                else:
                    colour = cell.colour
                
                #Draw each cell based on the colour and size
                x1 = rowIndex * cellSize
                y1 = columnIndex * cellSize
                x2 = (rowIndex + 1) * cellSize
                y2 = (columnIndex + 1) * cellSize
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour)

        self.root.update()

    def update(self, delay=0.005):
        # Add a small delay for more visibility on agent movement
        sleep(delay)
        self.draw()

    def measureSegregation(self):
        totalFraction = 0
        for agent in self.agents:
            similarNeighbors = 0
            totalNeighbors = 0

            #Check the 8 neighbours surrounding the agent
            xAxis = [-1, 0, 1]
            yAxis = [-1, 0, 1]
            x, y = agent.location
            for dx in xAxis:
                for dy in yAxis:
                    neighbourX = x + dx
                    neighbourY = y + dy
                    #If the neighbour is within the grid then check if it has the same colour as the agent
                    if (neighbourX >= 0 and neighbourX < self.width) and (neighbourY >= 0 and neighbourY < self.height):
                        neighbour = self.grid[neighbourX][neighbourY]
                        if neighbour is not None:
                            totalNeighbors += 1 #Increment the total number of neighbours if the cell is not empty
                            if neighbour.colour == agent.colour:
                                similarNeighbors += 1 #Increment the number of similar neighbours if the neighbour has the same colour as the agent
            
            #If the number of neighbours is greater than 0, calculate the fraction of similar neighbours
            if totalNeighbors > 0:
                fraction = similarNeighbors / totalNeighbors
            else:
                fraction = 0

            totalFraction += fraction
        return totalFraction / len(self.agents) #Return the mean fraction (in decimal form) of similar neighbours

    def run(self, steps):
        segregationValues = [] # Array to store the segregation value for each agent at each step

        #Check the 8 neighbours surrounding the agent
        xAxis = [-1, 0, 1]
        yAxis = [-1, 0, 1]
        for step in range(steps):
            agent = random.choice(self.agents) #Choose a random agent each step
            if not agent.happy:
                chosenLocations = random.sample(self.emptyCells, agent.k) #Choose k random empty locations 
                fractionSimilar = defaultdict(int)

                #Iterate through the empty locations and calculate the fraction of similar neighbours for those empty locations
                for newLocation in chosenLocations:
                    similarNeighbors = 0
                    totalNeighbors = 0
                    x, y = newLocation
                    for dx in xAxis:
                        for dy in yAxis:
                            neighbourX = x + dx
                            neighbourY = y + dy

                            #If the neighbour is within the grid then check if it has the same colour as the agent
                            if (neighbourX >= 0 and neighbourX < self.width) and (neighbourY >= 0 and neighbourY < self.height):
                                neighbour = self.grid[neighbourX][neighbourY]
                                if neighbour is not None:
                                    totalNeighbors += 1 #Increment the total number of neighbours if the cell is not empty
                                    if neighbour.colour == agent.colour:
                                        similarNeighbors += 1 #Increment the number of similar neighbours if the neighbour has the same colour as the agent

                    #If the number of neighbours is greater than 0, calculate the fraction of similar neighbours        
                    if totalNeighbors > 0:
                        fractionSimilar[newLocation] = similarNeighbors / totalNeighbors
                    else:
                        fractionSimilar[newLocation] = 0

                newLocation = max(fractionSimilar, key=fractionSimilar.get) #Set the new location to the empty location with the highest fraction of similar neighbours
                self.emptyCells.remove(newLocation)

                #Add the agent's old location to the empty cells array and set that grid location to None
                self.emptyCells.append(agent.location)
                self.grid[agent.location[0]][agent.location[1]] = None 
                self.grid[newLocation[0]][newLocation[1]] = agent
                agent.move(newLocation)
            self.update() #Draw the updated world

            segregationValues.append(self.measureSegregation()) #Append the decimal segregation values for the current step to the segregation values array
            self.root.title(f'Step {step+1}')  
            
        avgSegregation = sum(segregationValues) / len(segregationValues) #Divide the total of all the segregation values by the number of values(number of agents)
        print(f"Degree of Segregation: {avgSegregation*100 + 0.5:.2f}%")

# Create a new world
world = SchellingModelWorld(10, 10)

# Populate the world with 90 agents (since 10% of the 100 cells should be empty)
world.populate(nAgents=90, k=10)

# Run the simulation
world.run(400)

world.root.mainloop()
