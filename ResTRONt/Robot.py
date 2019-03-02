class Robot:
    ''' Represents the robot itself and its current state. '''

    def __init__(self):
        ''' Avoid using the default constructor. Use the json constructor instead '''

        self.pos = []
        self.robot_carry = {}
        self.next_objective  = []

    def __init__(self, json):
        ''' Initialize the robot given the instance json. '''

        self.pos = [json["payload"]["location"]["x"], json["payload"]["location"]["y"], \
            json["payload"]["direction"]]
        self.robot_carry = {'G': [], 'R': [], 'O': []}
        self.next_objective = ["", -1, -1, 0]
