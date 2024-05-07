import tkinter as tk
import random
from agents import XYEnvironment, Agent
class SchellingModel(XYEnvironment):
   def __init__(self, width=10, height=10, k=3):
       super().__init__(width, height)
       self.k = k
       self.grid = tk.Tk()
       self.grid.title("Schelling's Model of Segregation")
       self.canvas = tk.Canvas(self.grid, width=width*50, height=height*50)
       self.canvas.pack()
       self.create_grid()
       self.add_agents()
   def create_grid(self):
       for i in range(self.width):
           for j in range(self.height):
               x0, y0 = i*50, j*50
               x1, y1 = x0 + 50, y0 + 50
               self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
               self.canvas.create_text(x0 + 25, y0 + 25, text="({}, {})".format(i, j))
   def add_agents(self):
       # Place agents randomly
       for i in range(self.width):
           for j in range(self.height):
               if random.random() < 0.1:
                   continue  # Empty cell
               agent_color = 'red' if random.random() < 0.5 else 'blue'
               agent = Agent(program=self.agent_program)
               self.add_thing(agent, location=(i, j))
               self.canvas.create_oval(i*50, j*50, (i+1)*50, (j+1)*50, fill=agent_color)
   def agent_program(self, percept):
       # Agent's program
       similar_neighbors = sum(1 for neighbor in percept if neighbor['color'] == percept['color'])
       empty_neighbors = sum(1 for neighbor in percept if neighbor['color'] == 'empty')
       if empty_neighbors == 0:
           return 'stay'
       similar_fraction = similar_neighbors / (self.k + empty_neighbors)
       if similar_fraction > 0.5:
           return 'stay'
       else:
           empty_neighbors = [neighbor for neighbor in percept if neighbor['color'] == 'empty']
           return 'move', random.choice(empty_neighbors)['location']
   def step(self):
       agent = random.choice(self.agents)
       percept = self.get_percept(agent)
       action, location = agent.program(percept)
       if action == 'move':
           self.move_to(agent, location)
def run():
   model = SchellingModel()
   model.grid.mainloop()
run()