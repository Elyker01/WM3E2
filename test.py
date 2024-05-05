from agents import Agent
import random

class RationalVacuumAgent(Agent):
    def __init__(self, program=None):
        super().__init__(program)
        self.model = {loc_A: None, loc_B: None, loc_C: None, loc_D: None}

    def update_model(self, location, status):
        """Update the agent's model of the environment."""
        self.model[location] = status

    def can_grab(self, thing):
        """The agent can grab something if it is at the agent's location."""
        return thing.location == self.location

def RationalAgentProgram(percept):
    """Rational agent program for the vacuum environment."""
    location, status = percept

    # Update the agent's model based on the current percept
    agent.update_model(location, status)

    # If everything is clean, do NoOp
    if all(value == 'Clean' for value in agent.model.values()):
        return 'NoOp'

    # If the current location is dirty, suck
    if status == 'Dirty':
        return 'Suck'

    # Move to the nearest dirty location
    dirty_locations = [loc for loc, stat in agent.model.items() if stat == 'Dirty']
    nearest_dirty_location = min(dirty_locations, key=lambda loc: manhattan_distance(agent.location, loc))

    # Determine the optimal action to move towards the nearest dirty location
    optimal_action = determine_optimal_action(agent.location, nearest_dirty_location)

    return optimal_action

def manhattan_distance(location1, location2):
    """Calculate the Manhattan distance between two locations."""
    return abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])

def determine_optimal_action(current_location, target_location):
    """Determine the optimal action to move from the current location to the target location."""
    x_diff = target_location[0] - current_location[0]
    y_diff = target_location[1] - current_location[1]

    if x_diff > 0:
        return 'Right'
    elif x_diff < 0:
        return 'Left'
    elif y_diff > 0:
        return 'Up'
    elif y_diff < 0:
        return 'Down'
    else:
        return 'NoOp'  # No movement needed

# Create the rational agent with the rational agent program
agent = RationalVacuumAgent(program=RationalAgentProgram)

# Rest of the code remains the same as before
# ...

# Add the rational agent to the environment
env.add_thing(agent)

# Run the environment
env.run()

# Print the final state and performance
print("The agent has now cleaned everything:", format(env.status), "\n")
print("The agent's final score is", agent.performance, "meaning it has taken",
      (agent.performance + (-agent.performance * 2)), "steps to clean the whole environment.", "\n")
