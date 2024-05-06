# Importing required libraries
import heapq
import time

# Node class for representing states in the search tree
class Node:
    def __init__(self, state, action=None, cost=0, parent=None):
        """Initialize a node in the search tree."""
        self.state = state
        self.action = action
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        """Comparison method for nodes based on cost."""
        return self.cost < other.cost

def execute_action(state):
    """Define possible actions based on the agent's location."""
    # Calculate agent's row and column in the grid
    agent_index = state.index('Agent')
    agent_row, agent_col = divmod(agent_index, 3)

    # Determine possible actions based on agent's location
    possible_actions = []
    if agent_row > 0:
        possible_actions.append('Up')
    if agent_row < 2:
        possible_actions.append('Down')
    if agent_col > 0:
        possible_actions.append('Left')
    if agent_col < 2:
        possible_actions.append('Right')

    return possible_actions

def result(state, action):
    """Return the resulting state after taking an action."""
    # Get agent's current row and column
    agent_index = state.index('Agent')
    agent_row, agent_col = divmod(agent_index, 3)

    # Update agent's position based on the action
    if action == 'Up':
        new_agent_index = agent_index - 3
    elif action == 'Down':
        new_agent_index = agent_index + 3
    elif action == 'Left':
        new_agent_index = agent_index - 1
    elif action == 'Right':
        new_agent_index = agent_index + 1

    # Create a new state with updated agent position
    new_state = list(state)
    new_state[agent_index] = 'Clean'  # Agent cleans the current square
    new_state[new_agent_index] = 'Agent'  # Agent moves to the new square

    return tuple(new_state)

def cost(state, action):
    """Return the cost of taking an action."""
    return 1  # Cost of each action is 1

def is_goal(state):
    """Check if the state is the goal state."""
    return state == goal_state

def uniform_cost_search():
    """Uniform Cost Search algorithm."""
    frontier = []
    heapq.heappush(frontier, Node(initial_state))
    explored = set()

    # Explore states until the goal is found or no solution exists
    while frontier:
        node = heapq.heappop(frontier)
        state = node.state

        if is_goal(state):
            return node  # Goal state found

        explored.add(state)

        # Expand current node and add child nodes to the frontier
        for action in execute_action(state):
            child_state = result(state, action)
            child_cost = node.cost + cost(state, action)
            child_node = Node(child_state, action, child_cost, node)

            if child_state not in explored:
                heapq.heappush(frontier, child_node)

    return None  # Goal not found

def extract_solution(node):
    """Extract the solution path from the goal node."""
    actions = []
    while node.parent:
        actions.append(node.action)
        node = node.parent
    return actions[::-1]  # Reverse the actions to get the correct order

# Define initial and goal states
initial_state = ('Dirty', 'Dirty', 'Dirty',
                 'Clean', 'Agent', 'Clean',
                 'Clean', 'Clean', 'Clean')

goal_state = ('Clean', 'Clean', 'Clean',
              'Clean', 'Agent', 'Clean',
              'Clean', 'Clean', 'Clean')

# Measure execution time
start_time = time.time()
goal_node = uniform_cost_search()
end_time = time.time()
execution_time = end_time - start_time

# Output the results
if goal_node:
    solution = extract_solution(goal_node)
    print("Optimal sequence of actions:", solution)
    print("Number of actions:", len(solution))
    print("Total cost:", goal_node.cost)
    print("Execution time:", execution_time, "seconds")
else:
    print("Goal state not found.")
