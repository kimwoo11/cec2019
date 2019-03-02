class State(object):
    ''' State '''

    def __init__(self, data):
        data = data["payload"]["constants"]
        # Constants
        self.costQuery = data['TIME']
        self.bin_cap = {}
        self.total_trash = data['TOTAL_COUNT']\

        # Variables
        self.remaining_trash = {}
        self.bin_count = {0: 0, 1: 0, 2: 0}
        self.finished = False
        self.located_items = set()
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
        for i in range(len(curr_located_items)):
            if curr_located_items[i]['id'] not in self.located_items:
                self.located_items.add(curr_located_items[i]['id'])
                x = curr_located_items[i]['x']
                y = curr_located_items[i]['y']
                if 'U' in self.curr_map[y][x]:
                    print('Error: this should not be unexplored')
                elif 'E' in self.curr_map[y][x]:
                    self.curr_map[y][x]['E'].append((curr_located_items[i]['id'], curr_located_items[i]['type'][0]))
                else:
                    return "Big Error"

        finished = data['finished']
        if finished:
            self.finished = finished
