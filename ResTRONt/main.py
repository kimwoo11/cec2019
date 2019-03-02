from requests import Request
from ResTRONt.Robot import Robot
from ResTRONt.State import State
from ResTRONt.Decisions import Decisions
from ResTRONt.Actions import Actions

if __name__ == "__main__":
    print(Request.delete('instance'))
    json = Request.post('instance')
	curr_state = State.init_map(json)
	robot = Robot(json)

	while not curr_state.finished:
        # Get next instruction
		next_instr, x, y = Decisions.eval_function(curr_state, robot)

		# Robot executes next instruction if at target location
        if robot.pos[0:1] = x, y:
            # We are at the target location
            if next_instr == "scan":
                Actions.scan(curr_state, robot)
            elif next_instr == "unload":
                Actions.unload(curr_state)
            elif next_instr == "collect":
                Actions.collect(curr_state)
            else:
                print("Unknown command")

        else:
            Actions.move(curr_state, robot, x, y)
