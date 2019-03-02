class State(object):
    ''' State '''

    def __init__(self, data):
        data = data["payload"]["constants"]
        # Constants
        self.costQuery = data['TIME']
        self.bin_cap = {}

        # Variables
        self.remaining_trash = {}
        self.bin_count = {0: 0, 1: 0, 2: 0}
        self.finished = False
        self.num_located_items = 0
        self.bin_type = {0: 'G', 1: 'R', 2: 'O'}

        y = data["ROOM_DIMENSIONS"]["Y_MAX"]
        x = data["ROOM_DIMENSIONS"]["X_MAX"]
        self.curr_map = [[{'U': 'U'} for i in range(x+1)] for j in range(y+1)]
        # initialize the bin locations, the capacity of bins, and the reminaing_trash dictionary
        for i, b_type in enumerate(['GARBAGE', 'RECYCLE', 'ORGANIC']):
            x = data['BIN_LOCATION'][b_type]['X']
            y = data['BIN_LOCATION'][b_type]['Y']
            self.curr_map[y][x] = {'B': i}
            self.bin_cap[i] = data['BIN_CAPACITY'][b_type]
            self.remaining_trash[b_type[0]] = data['TOTAL_COUNT'][b_type]
        self.radius = data['SCAN_RADIUS']

    def update_map(self, data):  # updating the state
        data = data["payload"]
        curr_located_items = data['itemsLocated']
        num_new_located_items = len(curr_located_items) - self.num_located_items

        # we want to iterate through the curr_located_items from [n = number of located items from prior,
        # n + number of newly located items]
        for i in range(self.num_located_items, self.num_located_items + num_new_located_items):
            x = curr_located_items[i]['x']
            y = curr_located_items[i]['y']
            if 'U' in self.curr_map[y][x]:
                print('Error: this should not be unexplored')
            elif 'E' in self.curr_map[y][x]:
                self.curr_map[y][x]['E'].append((curr_located_items[i]['id'], curr_located_items[i]['type'][0]))
            else:
                return "Big Error"

        finished = data['payload']['finished']
        if finished:
            self.finished = finished
