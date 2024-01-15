from agents import TrivialVacuumEnvironment, Agent, RandomAgentProgram
import random



loc_A, loc_B, loc_C, loc_D = (0, 0), (1, 0), (0,1), (1,1)  # The four locations for the Vacuum world

class vacuumEnvironment(TrivialVacuumEnvironment):
    """This environment has four locations, A,B,C and D. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""
    def __init__(self):
        super().__init__()
        self.status = {loc_A: random.choice(["Clean", "Dirty"]),
                        loc_B: random.choice(["Clean", "Dirty"]),
                        loc_C: random.choice(["Clean", "Dirty"]),
                        loc_D: random.choice(["Clean", "Dirty"])}
        
    
    def execute_action(self,agent,action):
        """Change agent's location and/or location's status; track performance.
        Score -1 for each move."""
        if action == "Up":
            agent.performance -= 1
            if agent.location[1] < 1:
                agent.location = (agent.location[0], agent.location[1] + 1) # Add 1 to the y coordinates 


        elif action == "Right":
            agent.performance -= 1
            if agent.location[0] < 1:
                agent.location = (agent.location[0] + 1, agent.location[1]) # Add 1 to the x coordinates 


        elif action == "Left":
            agent.performance -= 1
            if agent.location[0] > 0:
                agent.location = (agent.location[0] - 1, agent.location[1]) # Minus 1 to the x coordinates
            

        elif action == "Down":
            agent.performance -= 1
            if agent.location[1] > 0:
                agent.location = (agent.location[0], agent.location[1] - 1) # Minus 1 to the y coordinates


        if action == "Suck":
            if self.status[agent.location] == "Dirty":
                self.status[agent.location] = "Clean"

        cleanLocations = [agentLocation for agentLocation, dirtyCleanStatus in self.status.items() if str(dirtyCleanStatus) == "Clean"]
        for location in cleanLocations:
            if random.random() <= 0.0000000001:
                self.status[location] = "Dirty"
        
    def default_location(self, thing):
        """Agents start in one of the four locations at random."""
        return random.choice([loc_A, loc_B, loc_C, loc_D])
    



if __name__ == "__main__":
    env = vacuumEnvironment()
    agent = Agent(program=RandomAgentProgram(["Up", "Right", "Left", "Down", "Suck"]))
    agent.location = random.choice([loc_A, loc_B, loc_C, loc_D])
    env.add_thing(agent)
    isClean = False


    print("The state of the environment locations are: {}. ", format(env.status), "\n")
    print("The agent's starting location is", format(agent.location) , "\n")


    while isClean == False:
        env.step()

        print("The state of the environment locations are:", format(env.status) , "\n")
        print("The agent is currently located at:", format(agent.location) , "\n")

        isClean = True
        for status in env.status: # If there are any dirty locations left after the agent has travelled to it, change the isClean status to false
            if env.status[status] == "Dirty":
                isClean = False



    print("The agent has now cleaned everything:", format(env.status) , "\n")
    print("The agent's final score is", agent.performance, "meaning it has taken", (agent.performance + (-agent.performance * 2)), "steps to clean the whole environment.", "\n")


