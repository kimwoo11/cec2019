import random
import math

class Decisions:

    def eval_function(State, Robot):
        """
        Function takes the game state and the state of the robot as input, and returns the next objective for the robot
        Also updates the Robot.nextObjective attribute to track the previously decided objective

        :param State: object of class State containing all relevant information about the instance
        :param Robot: object of class Robot containing relevant information about the state of the Robot
        :return: Returns an array containing the action string( either "Scan", "Collect" or "Unload") and
                 the target position to move to first
        """

        grid = State.grid
        min_trash = math.inf
        min_bin = math.inf
        trash_pos = None
        bin_pos = None
        bin_Pspace = 1
        bin_Pcarry = 1
        unexplored = 0
        trashy = 0
        momentum = 1

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                item_dir = grid[y][x]

                key = item_dir.keys()
                if "U" in key:
                    # unexplored
                    unexplored += 1

                if "B" in key:
                    # Bin Location
                    bin_id = item_dir['B']
                    bin_type = State.binType[bin_id]
                    # Navigation Cost
                    cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                    # Reduce cost based on current holdings of specific trash type and remaining space
                    # in the corresponding bin (relative space to normalize bins with different capacities)
                    cost -= bin_Pspace * math.abs(State.binCount[bin_id] - State.binCap[bin_id]) / State.binCap[bin_id]
                    cost -= bin_Pcarry * Robot.robotCarry[bin_type] / (1 + sum(Robot.robotCarry.values()))
                    cost -=

                    if cost < min_bin:
                        min_bin = cost
                        bin_pos = (x, y)

                if 'E' in key:
                    if item_dir['E'] != []:
                        # Not an empty list
                        empty = False
                        trashy += 1
                        # Some Trash Location
                        cost = nav_cost(Robot.pos, (x, y), State.costQuery)
                        if cost < min_trash:
                            min_trash = cost
                            trash_pos = (x, y)

        kc = 1
        ku = 1
        ks = 1

        if empty:
            scan_score = ks
            collect_score = 0
            unload_score = 0
        else:
            collect_score = kc / max(min_trash, 0.5)
            unload_score = ku / max(min_bin, 0.5)

            scan_score = ks * unexplored / len(State.grid) * len(State.grid[0]) * max(0.5, trashy)

        next_obj = Robot.nextObjective  # Current Robot Objective
        if next_obj[0] == 'Scan':
            scan_score += momentum * next_obj[3] / (scan_score + unload_score + collect_score)

        if next_obj[0] == 'Collect':
            collect_score += momentum * next_obj[3] / (scan_score + unload_score + collect_score)

        if next_obj[0] == 'Unload':
            unload_score += momentum * next_obj[3] / (scan_score + unload_score + collect_score)

        max_score = max(scan_score, collect_score, unload_score)  # Max score at current state

        # Check to see if the current suggestion is the same as current objective
        # If it is, add fraction to score

        if max_score == scan_score:
            randx = random.randint(0, len(grid[0]))
            randy = random.randint(0, len(grid))
            while 'U' not in grid[randx][randy].keys():
                randx = random.randint(0, len(grid[0]))
                randy = random.randint(0, len(grid))

            Robot.nextObjective = ["Scan", randx, randy, max_score]
            return ["Scan", randx, randy]

        if max_score == collect_score:
            Robot.nextObjective = ["Collect", trash_pos[0], trash_pos[1], max_score]
            return ["Collect", trash_pos[0], trash_pos[1]]

        if max_score == unload_score:
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
