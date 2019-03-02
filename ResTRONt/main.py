from requests import Request
from ResTRONt.Robot import *
from ResTRONt.State import *
from ResTRONt.util import *

if __name__ == "__main__":
    print(Request.get('instance'))
    print(Request.post('instance'))
    #instantiation = Request.post('instance')
