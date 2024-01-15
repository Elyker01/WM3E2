from agents import Agent
import random

from environment import vacuumEnvironment

loc_A, loc_B, loc_C, loc_D = (0, 0), (1, 0), (0, 1), (1, 1)

class RationalVacuumAgent(Agent):
    def __init__(self):
        super().__init__(program=self.rational_program)
        self.cleaned_locations = set()

    def rational_program(self, percept):
        # Extract location and status from the percept
        location, status = percept

        # Decision-making logic based on cleanliness status
        if status == 'Dirty':
            return 'Suck'  # If the current location is dirty, clean it
        elif location not in self.cleaned_locations:
            # If the location is unclean and hasn't been visited yet, move to the next unclean location
            self.cleaned_locations.add(location)
            return self.go_to_next_unclean_location(location)
        else:
            return 'NoOp'  # No operation if the location is already clean

    def go_to_next_unclean_location(self, current_location):
        # Find unclean locations that haven't been visited
        unclean_locations = [loc for loc, status in env.status.items() if status == 'Dirty' and loc not in self.cleaned_locations]

        if unclean_locations:
            # Choose the next unclean location based on Manhattan distance heuristic
            next_location = min(unclean_locations, key=lambda loc: self.manhattan_distance(current_location, loc))
            return self.get_action_to_reach(current_location, next_location)
        else:
            return 'NoOp'  # No more dirty locations to clean

    def manhattan_distance(self, x, y):
        # Calculate Manhattan distance between two locations
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def get_action_to_reach(self, current_location, target_location):
        # Determine the action to reach the target location based on relative coordinates
        if current_location[0] < target_location[0]:
            return 'Right'
        elif current_location[0] > target_location[0]:
            return 'Left'
        elif current_location[1] < target_location[1]:
            return 'Up'
        elif current_location[1] > target_location[1]:
            return 'Down'

# Your vacuumEnvironment class remains the same

if __name__ == "__main__":
    env = vacuumEnvironment()
    agent = RationalVacuumAgent()
    agent.location = random.choice([loc_A, loc_B, loc_C, loc_D])
    env.add_thing(agent)
    isClean = False

    print("The state of the environment locations are: {}.".format(env.status), "\n")
    print("The agent's starting location is", format(agent.location), "\n")

    while not isClean:
        env.step()
        print("The state of the environment locations are:", format(env.status), "\n")
        print("The agent is currently located at:", format(agent.location), "\n")

        # Check if all locations are clean to terminate the loop
        isClean = all(status == 'Clean' for status in env.status.values())

    print("The agent has now cleaned everything:", format(env.status), "\n")
    print("The agent's final score is", agent.performance, "meaning it has taken", (agent.performance + (-agent.performance * 2)),
          "steps to clean the whole environment.", "\n")
