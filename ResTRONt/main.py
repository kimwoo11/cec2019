from Requests import Request
from Robot import *
from State import *
from util import *

if __name__ == "__main__":
	data = Request.get('instance')
	curr_state = State.init_map(data)
	robot = Robot()	
	finished = data['payload']['finished']
	while not finished:
		next_instr = eval_function(curr_state, robot)
		# robot executes
		# state is updated
		