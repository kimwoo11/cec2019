import random
import math
from State import State
from Robot import Robot

class Decisions:
    def eval_function(self, state, robot):
        """
        Function takes the game state and the state of the robot as input, and returns the next objective for the robot
        Also updates the Robot.next_objective attribute to track the previously decided objective

        :param State: object of class State containing all relevant information about the instance
        :param Robot: object of class Robot containing relevant information about the state of the Robot
        :return: Returns an array containing the action string( either "Scan", "Collect" or "Unload") and
                 the target position to move to first
        """

        grid = state.curr_map
        min_trash = math.inf
        min_bin = math.inf
        trash_pos = None
        bin_pos = None
        empty = True
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
                    bin_type = state.bin_type[bin_id]
                    # Navigation Cost
                    cost = self.nav_cost(robot.pos, (x, y), state.costQuery)
                    # Reduce cost based on current holdings of specific trash type and remaining space
                    # in the corresponding bin (relative space to normalize bins with different capacities)
                    cost -= bin_Pspace * abs(state.bin_count[bin_id] - state.bin_cap[bin_id]) / state.bin_cap[bin_id]
                    tot = len(robot.robot_carry["G"]) + len(robot.robot_carry["R"]) + len(robot.robot_carry["O"])

                    cost -= bin_Pcarry * len(robot.robot_carry[bin_type]) / (1 + tot)

                    if cost < min_bin:
                        min_bin = cost
                        bin_pos = (x, y)

                if 'E' in key:
                    if item_dir['E'] != []:
                        # Not an empty list
                        empty = False
                        trashy += 1
                        # Some Trash Location
                        cost = self.nav_cost(robot.pos, (x, y), state.costQuery)
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

            scan_score = ks * unexplored / len(state.grid) * len(state.grid[0]) * max(0.5, trashy)

        next_obj = robot.next_objective  # Current robot Objective
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
            if next_obj[0] != "Scan":

                randx = random.randint(0, len(grid[0])-1)
                randy = random.randint(0, len(grid)-1)
                while 'U' not in grid[randy][randx].keys():
                    randx = random.randint(0, len(grid[0])-1)
                    randy = random.randint(0, len(grid)-1)

                robot.next_objective = ["Scan", randx, randy, max_score]
                print("Scan", randx, randy)
                return ["Scan", randx, randy]
            else:
                print(robot.next_objective[0:3])
                return robot.next_objective[0:3]

        if max_score == collect_score:
            robot.next_objective = ["Collect", trash_pos[0], trash_pos[1], max_score]
            print("Collect", trash_pos[0], trash_pos[1])
            return ["Collect", trash_pos[0], trash_pos[1]]

        if max_score == unload_score:
            robot.next_objective = ["Unload", bin_pos[0], bin_pos[1], max_score]
            print("Unload", bin_pos[0], bin_pos[1])
            return ["Unload", bin_pos[0], bin_pos[1]]

        print("eval_function error")
        return 0

    def nav_cost(self, curr, targ, costs):
        '''
        :param curr: Tuple containing current position and heading of the robot
        :param targ: Tuple containing position of target
        :param costs: Dictionary of query costs to move or turn
        :return: Minimum total cost to navigate from current Pose to target position
        '''

        # Manhattan Distance (number of Moves to target)
        manhattan = abs(curr[0]-targ[0]) + abs(curr[1]-targ[1])

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

        return manhattan*costs['MOVE'] + (horizontal+vertical)*costs['TURN']
