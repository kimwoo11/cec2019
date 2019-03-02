import random
import math


def eval_function(State, Robot):
    """
    Function takes the game state and the state of the robot as input, and returns the next objective for the robot
    Also updates the Robot.nextObjective attribute to track the previously decided objective

    :param State: object of class State containing all relevant information about the instance
    :param Robot: object of class Robot containing relevant information about the state of the Robot
    :return: Returns an array containing the action string( either "Scan", "Collect" or "Unload") and
             the target position to move to first
    """

    # Iterating through the list to find closest piece of trash, closest bin, and establish whether the list is either
    # fully empty or fully unexplored

    grid = State.grid
    empty = True
    min_trash = math.inf
    min_bin = math.inf
    trash_pos = None
    bin_pos = None

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            item_dir = grid[y][x]
            key = item_dir.keys()
            if 'E' not in key:
                # Not Empty
                if 'U' in key:
                    # Unexplored
                    pass
                elif "B" in key:
                    # Bin Location
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    if cost < min_bin:
                        min_bin = cost
                        bin_pos = (x, y)

                else:
                    # Some Trash Location
                    empty = False
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    if cost < min_trash:
                        min_trash = cost
                        trash_pos = (x, y)

    # Calculates the Heuristic Function score for each possible action
    scan_score = 0
    collect_score = 0
    unload_score = 0
    kc = 1
    ku = 1
    ks = 1
    if empty:
        scan_score = ks
    else:
        collect_score += kc/max(min_trash, 0.5)
        tot = sum(Robot.carry.values())
        if tot != 0:
            unload_score += ku/max(min_bin, 0.5)

    # Returns the optimal action and saves to Robot.next Objective
    max_score = max(scan_score, collect_score, unload_score)
    if max_score == scan_score:
        scan_spot = (random.randint(0, len(grid[y])), random.randint(0, len(grid)))
        Robot.nextObjective = ["Scan", scan_spot]
        return ["Scan", scan_spot]

    if max_score == collect_score:
        Robot.nextObjective = ["Collect", trash_pos]
        return ["Collect", trash_pos]

    if max_score == unload_score:
        Robot.nextObjective = ["Unload", bin_pos]
        return ["Unload", bin_pos]


def eval_2(State, Robot):

    grid = State.grid
    min_trash = math.inf
    min_bin = math.inf
    empty = True
    trash_pos = None
    bin_pos = None
    bin_Pspace = 1
    bin_Pcarry = 1

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            item_dir = grid[y][x]

            key = item_dir.keys()
            if 'E' not in key:
                # Not Empty
                if 'U' in key:
                    # unexplored
                    pass
                elif "B" in key:
                    # Bin Location
                    bin_id = item_dir['B']
                    bin_type = State.binType[bin_id]
                    # Navigation Cost
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    # Reduce cost based on current holdings of specific trash type and remaining space
                    # in the corresponding bin (relative space to normalize bins with different capacities)
                    cost -= bin_Pspace*math.abs(State.binCount[bin_id]-State.binCap[bin_id])/State.binCap[bin_id]
                    cost -= bin_Pcarry*Robot.robotCarry[bin_type]/(1 + sum(Robot.robotCarry.values()))

                    if cost < min_bin:
                        min_bin = cost
                        bin_pos = (x, y)

                else:
                    # Some Trash Location
                    empty = False
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    if cost < min_trash:
                        min_trash = cost
                        trash_pos = (x, y)

    scan_score = 0
    collect_score = 0
    unload_score = 0
    kc = 1
    ku = 1
    ks = 1
    if empty:
        scan_score = ks
    else:
        collect_score += kc / max(min_trash, 0.5)
        unload_score += ku / max(min_bin, 0.5)

    max_score = max(scan_score, collect_score, unload_score)
    if max_score == scan_score:
        scan_spot = (random.randint(0, len(grid[y])), random.randint(0, len(grid)))
        Robot.nextObjective = ["Scan", scan_spot]
        return ["Scan", scan_spot]

    if max_score == collect_score:
        Robot.nextObjective = ["Collect", trash_pos]
        return ["Collect", trash_pos]

    if max_score == unload_score:
        Robot.nextObjective = ["Unload", bin_pos]
        return ["Unload", bin_pos]

    return 0


def eval_3(State, Robot):

    grid = State.grid
    min_trash = math.inf
    min_bin = math.inf
    empty = True
    trash_pos = None
    bin_pos = None
    bin_Pspace = 1/2
    bin_Pcarry = 1/2
    mom_paramter = 1

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            item_dir = grid[y][x]

            key = item_dir.keys()
            if 'E' not in key:
                # Not Empty
                if 'U' in key:
                    # unexplored
                    pass
                elif "B" in key:
                    # Bin Location
                    bin_id = item_dir['B']
                    bin_type = State.binType[bin_id]
                    # Navigation Cost
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery) + 1
                    # Reduce cost based on current holdings of specific trash type and remaining space
                    # in the corresponding bin (relative space to normalize bins with different capacities)
                    cost -= bin_Pspace * math.abs(State.binCount[bin_id] - State.binCap[bin_id]) / State.binCap[bin_id]
                    cost -= bin_Pcarry * Robot.robotCarry[bin_type] / (1 + sum(Robot.robotCarry.values()))

                    if cost < min_bin:
                        min_bin = cost
                        bin_pos = (x, y)

                else:
                    # Some Trash Location
                    empty = False
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    if cost < min_trash:
                        min_trash = cost
                        trash_pos = (x, y)

    scan_score = 0
    collect_score = 0
    unload_score = 0
    kc = 1
    ku = 1
    ks = 1
    if empty:
        scan_score = ks
    else:
        collect_score += kc / max(min_trash, 0.5)
        unload_score += ku / max(min_bin, 0.5)

    max_score = max(scan_score, collect_score, unload_score)    # Max score at current state
    next_obj = Robot.nextObjective                              # Current Robot Objective

    # Check to see if the current suggestion is the same as current objective
    # If it is, add fraction to score

    # First Trial (score == 0), assign based on maximum
    if next_obj[3] == 0:
        if max_score == scan_score:
            scan_spot = (random.randint(0, len(grid[y])), random.randint(0, len(grid)))
            Robot.nextObjective = ["Scan", scan_spot[0], scan_spot[1], max_score]
            return ["Scan", scan_spot[0], scan_spot[1]]

        if max_score == collect_score:
            Robot.nextObjective = ["Collect", trash_pos[0], trash_pos[1], max_score]
            return ["Collect", trash_pos[0], trash_pos[1]]

        if max_score == unload_score:
            Robot.nextObjective = ["Unload", bin_pos[0], bin_pos[1], max_score]
            return ["Unload", bin_pos[0], bin_pos[1]]

    # Not the first trial, add momentum based on fractional difference between scores
    else:
        momentum_delta = mom_paramter*max_score/(scan_score + collect_score + unload_score + 1)

        if max_score == scan_score:
            if next_obj[0] == 'Scan':
                scan_spot = (random.randint(0, len(grid[y])), random.randint(0, len(grid)))
                Robot.nextObjective = ["Scan", scan_spot[0], scan_spot[1], max_score + momentum_delta]
                return ["Scan", scan_spot[0], scan_spot[1]]

            elif max_score >= next_obj[3]:
                scan_spot = (random.randint(0, len(grid[y])), random.randint(0, len(grid)))
                Robot.nextObjective = ["Scan", scan_spot[0], scan_spot[1], max_score]
                return ["Scan", scan_spot[0], scan_spot[1]]

        if max_score == collect_score:
            if next_obj[0] == 'Collect':
                Robot.nextObjective = ["Collect", trash_pos[0], trash_pos[1], max_score + momentum_delta]
                return ["Collect", trash_pos[0], trash_pos[1]]

            elif max_score >= next_obj[3]:
                Robot.nextObjective = ["Collect", trash_pos[0], trash_pos[1], max_score]
                return ["Collect", trash_pos[0], trash_pos[1]]

        if max_score == unload_score:
            if next_obj[0] == 'Unload':
                Robot.nextObjective = ["Unload", bin_pos[0], bin_pos[1], max_score + momentum_delta]
                return ["Unload", bin_pos[0], bin_pos[1]]
            elif max_score >= next_obj[3]:
                Robot.nextObjective = ["Unload", bin_pos[0], bin_pos[1], max_score]
                return ["Unload", bin_pos[0], bin_pos[1]]

    return 0


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
