class State():
    ''' State '''
    def __init__(self):
        curr_map = []
        costQuary = {}
        remaining_trash = {}
        time_spent = 0
        time_to_collect = 0
        bin_cap = {}
        bin_count = {0: 0, 1:0, 2:0}
        finished = False

    def init_map(self, data):
        data = data["payload"]["constants"]
        y = data["ROOM_DIMENSIONS"]["Y_MAX"]
        x = data["ROOM_DIMENSIONS"]["X_MAX"]
        self.curr_map = [[{'U': 'U'} for i in range(x)] for j in range(y)]
        for i, b_type in enumerate(['GARABAGE', 'RECYCLE', 'ORGANIC']):
            x = data['BIN_LOCATION'][b_type]['X']
            y = data['BIN_LOCATION'][b_type]['Y']
            self.curr_map[y][x] = {'B': i}
            self.bin_cap[i, data['BIN_CAPACITY'][b_type]]
            self.remaining_trash[i, data['BIN_CAPACITY']]

    def update_map(self, data):
        data = data["payload"]["constants"]

