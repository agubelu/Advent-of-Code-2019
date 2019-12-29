from collections import namedtuple, defaultdict
from etc.tupledict import TupleDict
from queue import PriorityQueue
from math import inf as INF

STEPS = [(1,0), (-1,0), (0,1), (0,-1)]

### Data types
KeyDistance = namedtuple('KeyDistance', 'distance doors')
MazePath = namedtuple('MazePath', 'x y distance doors')
class State(namedtuple('State', 'keys last_keys')):
    def __hash__(self):
        return hash(frozenset(self.keys)) ^ hash(frozenset(set(self.last_keys)))


positions = {}
maze = {}

### Read and parse the maze
with open("input/day18.txt") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            maze[x,y] = char
            if char.islower() or char.startswith('@'):
                positions[char] = (x, y)

KEYS = [k for k in positions if k.islower()]
N_KEYS = len(KEYS)
INITIAL_POS = positions["@"]

### Compute distances between key pairs
def compute_distances(grid, initials):
    distance_keys_aux = TupleDict()

    for origin in initials + KEYS:
        visited = {positions[origin]: 1}

        x, y = positions[origin]
        paths = [MazePath(x, y, 0, [])]

        while paths:
            new_paths = []
            for path in paths:
                for step in STEPS:
                    last_doors = path.doors.copy()
                    newx, newy = path.x + step[0], path.y + step[1]
                    if (newx, newy) in visited: continue
                    visited[newx, newy] = 1
                    val = grid.get((newx, newy), "#")

                    if val == "#":
                        continue
                    elif val.islower() and (origin, val) not in distance_keys_aux:
                        distance_keys_aux[origin, val] = KeyDistance(path.distance + 1, set(x.lower() for x in last_doors))
                    elif val.isupper():
                        last_doors.append(val)

                    new_paths.append(MazePath(newx, newy, path.distance + 1, last_doors))
            paths = new_paths

    ### Aux dict
    distance_keys = {}
    for (k1, k2), val in distance_keys_aux.items():
        distance_keys[k1, k2] = val
        distance_keys[k2, k1] = val
    return distance_keys

### Aux method for finding which key has been collected
def get_dist_keys(lks1, lks2, key_distance):
    for k1, k2 in zip(lks1, lks2):
        if k1 != k2:
            return key_distance[k1, k2].distance

### Generate neighbor nodes
def next_states(state, key_distance):
    paths = []

    for i, source in enumerate(state.last_keys):
        for k in KEYS:
            if k != source and (source, k) in key_distance:
                dist_data = key_distance[source, k]
                if k not in state.keys and dist_data.doors.issubset(state.keys):
                    last = state.last_keys.copy()
                    last[i] = k
                    paths.append(State(state.keys.union({k}), last))
    
    return paths

### Dijkstra algorithm
def find_shortest_path(initial, key_distance):
    distances = defaultdict(lambda: INF)
    q = PriorityQueue()
    distances[initial] = 0
    q.put((0, initial))

    while not q.empty():
        distu, u = q.get()
        if len(u.keys) == N_KEYS:
            return distances[u]
        for v in next_states(u, key_distance):
            alt = distu + get_dist_keys(u.last_keys, v.last_keys, key_distance)
            if alt < distances[v]:
                distances[v] = alt
                q.put((alt, v))

#### Part 1
distance_keys = compute_distances(maze, ["@"])
initial_state = State(set(), ['@'])
print(find_shortest_path(initial_state, distance_keys))

#### Part 2
maze[INITIAL_POS] = "#"
for stepx, stepy in STEPS:
    maze[INITIAL_POS[0] + stepx, INITIAL_POS[1] + stepy] = "#"
for i, (stepx, stepy) in enumerate([(1,1), (1,-1), (-1,1), (-1,-1)], start=1):
    posx, posy = INITIAL_POS[0] + stepx, INITIAL_POS[1] + stepy
    maze[posx, posy] = f"@{i}"
    positions[f"@{i}"] = (posx, posy)

distance_keys = compute_distances(maze, ["@1", "@2", "@3", "@4"])
initial_state = State(set(), ["@1", "@2", "@3", "@4"])
print(find_shortest_path(initial_state, distance_keys))