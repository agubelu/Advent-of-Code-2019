import math
from operator import itemgetter

def get_step(pos1, pos2):
    xdiff, ydiff = pos2[0] - pos1[0], pos2[1] - pos1[1]

    if xdiff == 0:
        step = (0, 1 if ydiff > 0 else -1)
    elif ydiff == 0:
        step = (1 if xdiff > 0 else -1, 0)
    else:
        gcd = math.gcd(abs(xdiff), abs(ydiff))
        step = (xdiff // gcd, ydiff // gcd)

    return step

def get_intermediate_spots(pos1, pos2):
    step = get_step(pos1, pos2)
    spots = []
    pos = (pos1[0] + step[0], pos1[1] + step[1])

    while pos != pos2:
        spots.append(pos)
        pos = (pos[0] + step[0], pos[1] + step[1])

    return spots

def has_line_of_sight(ast1, ast2, grid):
    if ast1 == ast2: return False
    spots = get_intermediate_spots(ast1, ast2)
    if not spots: return True
    if any(grid[y][x] for x, y in spots): return False
    return True

def get_polar_coords(ast1, ast2):
    try:
        # Get the (x,y) of ast2 relative to ast1 considering that the absolute (0,0) is in the top-left corner
        x = ast2[0] - ast1[0]
        y = ast1[1] - ast2[1]
        angle = math.pi / 2 - math.atan2(y, x)
    except ZeroDivisionError:
        angle = 0.0

    dist = math.sqrt((ast2[0] - ast1[0]) ** 2 + (ast2[1] - ast1[1]) ** 2)

    if angle < 0:
        angle = 2*math.pi + angle

    return angle, dist

grid = []
asteroids = []

#### Parsing
with open("input/day10.txt") as f:
    for y, line in enumerate(f):
        grid_line = []
        for x, char in enumerate(line.strip()):
            if char == "#":
                asteroids.append((x, y))
                grid_line.append(1)
            else:
                grid_line.append(0)
        grid.append(grid_line)
N_ASTEROIDS = len(asteroids)

#### Part 1
max_in_sight = 0
best_position = None

for station in asteroids:
    in_sight = 0
    for i, asteroid in enumerate(asteroids):
        # Reducing the search space
        if in_sight + N_ASTEROIDS - i < max_in_sight:
            break
        
        if has_line_of_sight(station, asteroid, grid):
            in_sight += 1

    if in_sight > max_in_sight:
        max_in_sight = in_sight
        best_position = station

print(best_position, max_in_sight)

#### Part 2
asteroids.remove(best_position)
asteroids = [(ast, get_polar_coords(best_position, ast)) for ast in asteroids]
asteroids.sort(key=itemgetter(1))

vaporized = []

while asteroids:
    last_angle = -999
    asteroids_to_delete = []

    for ast, (angle, dist) in asteroids:
        if angle == last_angle:
            continue
        else:
            last_angle = angle

        if has_line_of_sight(best_position, ast, grid):
            vaporized.append(ast)
            asteroids_to_delete.append((ast, (angle, dist)))
            grid[ast[1]][ast[0]] = 0

    for ast in asteroids_to_delete:
        asteroids.remove(ast)

vaporized200 = vaporized[199]
print(vaporized200[0] * 100 + vaporized200[1])

        
