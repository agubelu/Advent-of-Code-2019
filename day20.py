from string import ascii_uppercase
import sys
sys.setrecursionlimit(int(1e7))

maze = {}
portals = {}
dims = {}

STEPS = {'U': (0, -1), 'D': (0, +1), 'R': (+1, 0), 'L': (-1, 0)}
OPPOSITE_STEPS = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R', None: None}

global best_steps
best_steps = 1e99

# Read the maze
with open("input/day20.txt") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line):
            maze[x, y] = char

HEIGHT = max(y for _, y in maze.keys()) + 1
WIDTH = max(x for x, _ in maze.keys()) + 1

# Process the portals
inner = []
outer = []

for y in range(HEIGHT):
    for x in range(WIDTH):
        if maze.get((x, y), "#") not in ascii_uppercase: continue
        char1 = maze[x, y]
        if maze[x+1, y] in ascii_uppercase:
            # Horizontal portal
            char2 = maze[x+1, y]
            name = f"{char1}{char2}"
            if maze.get((x+2, y), "#") == ".":
                # Path to the right
                maze[x, y] = "#"
                maze[x+1, y] = name if name not in ("AA", "ZZ") else "#"
                portals[name] = portals.get(name, []) + [(x+2, y)]
                if maze.get((x-1, y), "#") == " ": inner.append((x+2, y))
                else: outer.append((x+2, y))
            elif maze.get((x-1, y), "#") == ".":
                # Path to the left
                maze[x+1, y] = "#"
                maze[x, y] = name if name not in ("AA", "ZZ") else "#"
                portals[name] = portals.get(name, []) + [(x-1, y)]
                if maze.get((x+2, y), "#") == " ": inner.append((x-1, y))
                else: outer.append((x-1, y))
        elif maze[x, y+1] in ascii_uppercase:
            # Vertical portal
            char2 = maze[x, y+1]
            name = f"{char1}{char2}"
            if maze.get((x, y+2), "#") == ".":
                # Path down
                maze[x, y] = "#"
                maze[x, y+1] = name if name not in ("AA", "ZZ") else "#"
                portals[name] = portals.get(name, []) + [(x, y+2)]
                if maze.get((x, y-1), "#") == " ": inner.append((x, y+2))
                else: outer.append((x, y+2))
            elif maze.get((x, y-1), "#") == ".":
                # Path up
                maze[x, y+1] = "#"
                maze[x, y] = name if name not in ("AA", "ZZ") else "#"
                portals[name] = portals.get(name, []) + [(x, y-1)]
                if maze.get((x, y+2), "#") == " ": inner.append((x, y-1))
                else: outer.append((x, y-1))

AA_POS = portals["AA"][0]
ZZ_POS = portals["ZZ"][0]
del portals["AA"]
del portals["ZZ"]

def get_available_dirs(x, y, previous, used_portals):
    res = [x for x in STEPS if x != OPPOSITE_STEPS[previous]]
    if 'U' in res:
        char = maze.get((x, y-1), "#")
        if char == "#" or char in used_portals: res.remove('U')
    if 'D' in res:
        char = maze.get((x, y+1), "#")
        if char == "#" or char in used_portals: res.remove('D')
    if 'R' in res:
        char = maze.get((x+1, y), "#")
        if char == "#" or char in used_portals: res.remove('R')
    if 'L' in res:
        char = maze.get((x-1, y), "#")
        if char == "#" or char in used_portals: res.remove('L')
    return res

def find_portal(name, xpos, ypos):
    portal_data = portals[name]
    if portal_data[0] == (xpos, ypos):
        return portal_data[1]
    else:
        return portal_data[0]

def dfs(x, y, depth=0, used_portals=[], previous_dir=None):
    global best_steps
    dirs = get_available_dirs(x, y, previous_dir, used_portals)

    for direction in dirs:
        step = STEPS[direction]
        aux = x, y
        next_x = x + step[0]
        next_y = y + step[1]
        next_tile = maze[next_x, next_y]

        if next_tile in portals:
            next_x, next_y = find_portal(next_tile, x, y)
            used_portals += [next_tile]
            direction = None
 
        x = next_x
        y = next_y
        if (x, y) == ZZ_POS and depth < best_steps:
            best_steps = depth + 1

        dfs(x, y, depth + 1, used_portals.copy(), direction)
        x, y = aux

dfs(*AA_POS)
print(best_steps)

#### Part 2
# Sit back and wait...
def get_maze(i):
    if i not in dims:
        dims[i] = maze.copy()
    return dims[i]

get_maze(0)[AA_POS] = "O"
last_changed = [(*AA_POS, 0)]
steps = 0

while get_maze(0)[ZZ_POS] != "O":
    steps += 1
    new_changes = []

    for x, y, dim in last_changed:
        for stepx, stepy in STEPS.values():
            newx, newy = x + stepx, y + stepy
            val = get_maze(dim)[newx, newy]
            if val == ".":
                new_changes.append((newx, newy, dim))
            elif val not in ("AA", "ZZ") and val in portals:
                isouter = (x, y) in outer
                if dim == 0 and isouter: continue
                outx, outy = find_portal(val, x, y)
                new_changes.append((outx, outy, dim-1 if isouter else dim+1))
    
    for x, y, dim in new_changes:
        get_maze(dim)[x, y] = "O"

    last_changed = new_changes

print(steps)
