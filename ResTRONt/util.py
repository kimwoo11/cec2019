import random


def eval_function(State, Robot):
    """ Function takes the game state and the state of the robot as input, and returns the next objective for the robot
    Also updates the Robot.nextObjective attribute to track the previously decided objective """
    grid = State.grid
    empty = True
    min_trash = 10000
    min_bin = 10000
    trash_pos = None
    bin_pos = None

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            item_dir = grid[y][x]
            # trash = []
            key = item_dir.keys()
            if 'E' not in key:
                # Not Empty
                if 'U' in key:
                    # unexplored
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
                    cost = nav_cost(Robot.pos,(x,y),State.costQuery)
                    if cost < min_trash:
                        min_trash = cost
                        trash_pos = (x,y)

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
        unload_score += ku/max(min_bin, 0.5)

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

