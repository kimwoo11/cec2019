from requests import Request
from ResTRONt.Robot import *
from ResTRONt.State import *
from ResTRONt.util import *

if __name__ == "__main__":
    print(Request.delete('instance'))
    json = Request.post('instance')
    #instantiation = Request.post('instance')
    r = Robot(json)
    print(r.pos)
    print(r.robot_carry)
    print(r.next_objective)

	data = Request.get('instance')
	curr_state = State.init_map(data)
	robot = Robot()
	finished = data['payload']['finished']
	while not finished:
		next_instr = eval_function(curr_state, robot)
		# robot executes
		# state is updated
