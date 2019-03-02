class Robot:
    ''' Represents the robot itself and its current state. '''

    def __init__(self):
        ''' Avoid using the default constructor. Use the json constructor instead '''
        
        pos = []
        robot_carry = {}
        next_objective  = []

    def __init__(self, json):
        ''' Initialize the robot given the instance json. '''

        pos = [json["payload"]["location"]["x"], json["payload"]["location"]["y"] \
            json["payload"]["direction"]]
        robot_carry = {'G': 0, 'R': 0, 'O': 0}
        next_objective = ["", -1, -1]
