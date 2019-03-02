from Requests import Request
from Robot import *
from State import *
from util import *

if __name__ == "__main__":
    print(Request.get('instance'))
    print(Request.post('instance'))
    #instantiation = Request.post('instance')
