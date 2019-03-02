

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
