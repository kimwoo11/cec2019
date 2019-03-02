from Request import Request
from State import State

class Actions:
    def __init__(self):
        pass
    def scan(self, curr_state, x, y):
        json = Request.post('scanArea')
        # UPDATE TO EXPLORED
        for i in range(x - curr_state.radius, x + curr_state.radius + 1):
            for j in range(y - curr_state.radius, y + curr_state.radius + 1):
                if i > 0 and j > 0 and i < len(curr_state.curr_map[0]) and j < len(curr_state.curr_map)\
                and (abs(x - i) + abs(y-j) <= curr_state.radius):
                    if 'U' in curr_state.curr_map[j][i]:
                        curr_state.curr_map[j][i].pop('U', None)
                        curr_state.curr_map[j][i]['E'] = []
        curr_state.update_map(json)
        pass

    def unload(self, curr_state, robot, x, y):
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

    def collect(self, curr_state, robot, x, y):
        while(curr_state.curr_map[y][x]['E'].len != 0):
            while(curr_state.curr_map[y][x]['E'].len != 0):
                robot[curr_state.curr_map[y][x]['E'][-1][1]].append(curr_state.curr_map[y][x]['E'][-1][0])
                curr_state.remaining_trash[curr_state.curr_map[y][x]['E'][-1][1]] -= 1
                json = Request.post('collectItem', curr_state.curr_map[y][x]['E'][-1][0])
                del curr_state.curr_map[y][x]['E'][-1]
            self.scan(curr_state, x, y)

        pass

    def move(self, curr_state, robot, x, y):
        curr_x, curr_y, curr_dir = robot.pos
        dir1 = ''
        dir2 = ''
        if x > curr_x:
            dir1 = 'E'
        elif x < curr_x:
            dir1 = 'W'
        if y < curr_y:
            dir2 = 'S'
        elif y > curr_y:
            dir2 = 'N'

        print('curr_x: ', curr_x)
        print('curr_y: ', curr_y)
        print('target x: ', x)
        print('target y: ', y)


        if dir1 == curr_dir or dir2 == curr_dir:
            #print("Right Heading")
            json = Request.post('move')
            if(curr_dir == 'N'):
                robot.pos[1] += 1
            if (curr_dir == 'S'):
                robot.pos[1] -= 1
            if (curr_dir == 'E'):
                robot.pos[0] += 1
            if (curr_dir == 'W'):
                robot.pos[0] -= 1
        else:
            if dir1 != '':
                json = Request.post('turn', dir1)
                robot.pos[2] = dir1
            else:
                json = Request.post('turn', dir2)
                robot.pos[2] = dir2
