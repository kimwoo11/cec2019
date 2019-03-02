from Requests import Request
from State import State
from math import abs

class Actions:
    def scan(curr_state, x, y):
        json = Request.post('scanArea')
        # UPDATE TO EXPLORED
        for i in range(x - curr_state.scan_radius, x + curr_state.scan_radius + 1):
            for j in range(y - curr_state.scan_radius, y + curr_state.scan_radius + 1):
                if i > 0 && j > 0 && i < curr_state.curr_map[0].len() && j < curr_state.curr_map.len()\
                && (abs(x - i) + abs(y-j) <= scan_radius):
                    if 'U' in curr_state.curr_map[j][i]:
                        curr_state.curr_map[j][i].pop('U', None)
                        curr_state.curr_map[j][i]['E'] = []
        update_map(json)
        pass

    def unload(curr_state):
        if curr_state.curr_map[y][x]['B'] == 0:
            type = 'G'
        if curr_state.curr_map[y][x]['B'] == 1:
            type = 'R'
        if curr_state.curr_map[y][x]['B'] == 2:
            type = 'O'

        for id in robot.robot_carry[type]:
            json = Request.post('unloadItem', id)
            curr_state.bin_count[id] += 1
        robot.robot_carry[type] = []

        pass

    def collect(curr_state, robot, x, y):
        while(curr_state.curr_map[y][x]['E'].len != 0):
            while(curr_state.curr_map[y][x]['E'].len != 0):
                robot[curr_state.curr_map[y][x]['E'][-1][1]].append(curr_state.curr_map[y][x]['E'][-1][0])
                curr_state.remaining_trash[curr_state.curr_map[y][x]['E'][-1][1]] -= 1
                json = Request.post('collectItem', curr_state.curr_map[y][x]['E'][-1][0])
                del curr_state.curr_map[y][x]['E'][-1]
            scan(curr_state, x, y)

        pass

    def move(curr_state, robot, x, y):
        curr_x, curr_y, curr_dir = robot.pos
        dir1 = ''
        dir2 = ''
        if x > curr_x:
            dir1 = 'E'
        elif x < curr_x:
            dir1 = 'W'
        if y > curr_y:
            dir2 = 'S'
        elif y < curr_y:
            dir2 = 'N'

        if dir1 == '' or dir2 == '' or dir1 == curr_dir or dir2 == curr_dir:
            json = Request.post('move')
        else:
            if dir1 != '':
                json = Request.post('turn', dir1)
            else:
                json = Request.post('turn', dir2)
