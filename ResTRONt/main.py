import requests

from Request import Request
from Robot import Robot
from State import State
from Decisions import Decisions
from Actions import Actions

if __name__ == "__main__":
    print(Request.delete('instance'))
    json = Request.post('instance')
    if json == -1:
        print("No JSON")
    curr_state = State(json)

    c_map = curr_state.curr_map

    robot = Robot(json)

    while not curr_state.finished:
        # Get next instruction
        [next_instr, x, y] = Decisions().eval_function(state=curr_state, robot=robot)
        print(next_instr, x, y)

        print("Next instruction: ", next_instr)
        print("Target x: ", x)
        print("Target y: ", y)
        print("Current x: ", robot.pos[0])
        print("Current y: ", robot.pos[1])
        print("Current direction: ", robot.pos[2])

        # Robot executes next instruction if at target location
        if robot.pos[0:1] == (x, y):
            # We are at the target location
            # print("Next instruction: ", next_instr)
            # print("Target x: ", x)
            # print("Target y: ", y)
            print("hey")

            if next_instr == "scan":
                Actions.scan(curr_state, x, y)
            elif next_instr == "unload":
                Actions.unload(curr_state, robot, x, y)
            elif next_instr == "collect":
                Actions.collect(curr_state, robot, x, y)
            else:
                print("Unknown command")

        else:
            Actions().move(curr_state, robot, x, y)
