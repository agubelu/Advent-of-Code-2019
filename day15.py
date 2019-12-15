from etc.intcode import from_file

comp = from_file("input/day15.txt")
tiles = {(0,0): 1}
STEPS = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0),}
STEPS_COMP = {'U': 1, 'D': 2, 'L': 3, 'R': 4}
OPPOSITE_STEPS = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R', None: None}

def get_available_dirs(previous, x, y):
    res = [x for x in STEPS if x != OPPOSITE_STEPS[previous]]
    if 'U' in res and not tiles.get((x, y+1), 1): res.remove('U')
    if 'D' in res and not tiles.get((x, y-1), 1): res.remove('D')
    if 'R' in res and not tiles.get((x+1, y), 1): res.remove('R')
    if 'L' in res and not tiles.get((x-1, y), 1): res.remove('L')
    return res

def try_move(direction):
    comp.set_inputs([STEPS_COMP[direction]])
    return comp.get_next_output()

def dfs(depth, previous_dir, x, y):
    dirs = get_available_dirs(previous_dir, x, y)
    for direction in dirs:
        move_result = try_move(direction)

        x += STEPS[direction][0]
        y += STEPS[direction][1]
        if (x,y) not in tiles: tiles[(x,y)] = move_result

        if move_result:
            if move_result == 2: print(depth)
            dfs(depth+1, direction, x, y)
            try_move(OPPOSITE_STEPS[direction])

        x -= STEPS[direction][0]
        y -= STEPS[direction][1]

dfs(1, None, 0, 0)

#### Part 2
minutes = 0
while any(z == 1 for z in tiles.values()):
    changes = {}
    for (x, y), val in tiles.items():
        if val != 2: continue
        if tiles.get((x+1, y), 1) == 1: changes[(x+1, y)] = 2
        if tiles.get((x-1, y), 1) == 1: changes[(x-1, y)] = 2
        if tiles.get((x, y+1), 1) == 1: changes[(x, y+1)] = 2
        if tiles.get((x, y-1), 1) == 1: changes[(x, y-1)] = 2
    for (x, y), val in changes.items():
        tiles[(x,y)] = val
    minutes += 1

print(minutes)