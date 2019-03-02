from Requests import Request
from Robot import *
from State import *
from util import *

if __name__ == "__main__":
    print(Request.delete('instance'))
    json = Request.post('instance')
    #instantiation = Request.post('instance')
    r = Robot(json)
    print(r.pos)
    print(r.robot_carry)
    print(r.next_objective)
