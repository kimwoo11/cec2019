import math

# Function takes the game state and the state of the robot as input, and returns the next objective for the robot
# Also updates the Robot.nextObjective attribute to track the previously decided objective
def eval_function(State, Robot):

    grid = State.grid
    empty = True
    min_trash

    for y in grid:
        for coord in y:
            trash = []
            key = coord.keys()
            if 'E' not in key:
                # Not Empty
                if 'U' in key:
                    # unexplored

                for trash in key:
                    trash





def nav_cost(curr, targ, costs):
    '''
    :param curr: Tuple containing current position and heading of the robot
    :param targ: Tuple containing position of target
    :param costs: Dictionary of query costs to move or turn
    :return: Minimum total cost to navigate from current Pose to target position
    '''

    # Manhattan Distance (number of Moves to target)
    manhattan = math.abs(curr[0]-targ[0]) + math.abs(curr[1]-targ[1])

    # Direction vector from current location to target
    dx = targ[0]-curr[0]
    dy = targ[1]-curr[1]
    rob_dir = curr[2]           # Robot heading

    horizontal = 0
    vertical = 0
    if rob_dir == 'N':          # Facing North
        if dy == -1:                # Will have to turn south
            vertical = 1
        if dx != 0:                 # Will have to turn east or west
            horizontal = 1
    elif rob_dir == 'S':        # Facing South
        if dy == 1:                 # Will have to turn north
            vertical = 1
        if dx != 0:                 # Will have to turn east or west
            horizontal = 1
    elif rob_dir == 'E':        # Facing East
        if dx == -1:                # Will have to turn west
            horizontal = 1
        if dy != 0:                 # Will have to turn north or south
            vertical = 1
    elif rob_dir == 'W':        # Facing West
        if dx == 1:                 # Will have to turn east
            horizontal = 1
        if dy != 0:                 # Will have to turn north or south
            vertical = 1

    return manhattan*costs['Move'] + (horizontal+vertical)*costs['Turn']