from etc.intcode import IntcodeComputer
import re

code = [int(x) for x in open("input/day17.txt").read().strip().split(",")]
comp = IntcodeComputer(code.copy())

grid = []
row = ""
x = y = 0
robot_pos = None
robot_heading = None
while True:
    char = chr(comp.get_next_output())
    if char in ("^", "v", "<", ">"): 
        robot_pos = (x-1, y)
        robot_heading = char
    if char == "\n":
        if row:
            grid.append(row)
            row = ""
            y += 1; x = 0
    else:
        row += char
    x += 1
    if comp.finished: break

width = len(grid[0])
height = len(grid)

#### Part 1
total = 0

for x in range(1, width-1):
    for y in range(1, height-1):
        coords_check = [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if all(grid[j][i] == "#" for i, j in coords_check):
            total += x * y

print(total)

#### Part 2
DIRS = {  # +1 turn right, -1 turn left
    0: (0, -1),  # Up
    1: (1, 0),   # Right
    2: (0, 1),   # Down
    3: (-1, 0)   # Left
}
robot_heading = {"^": 0, "v": 2, "<": 3, ">": 1}[robot_heading]

def get_path(grid, pos, heading):
    coors_left = pos[0] + DIRS[(heading - 1 ) % 4][0], pos[1] + DIRS[(heading - 1 ) % 4][1]
    coors_right = pos[0] + DIRS[(heading + 1 ) % 4][0], pos[1] + DIRS[(heading + 1 ) % 4][1]
    new_heading = None
    turn = None

    try:
        if grid[coors_left[1]][coors_left[0]] == "#":
            new_heading = (heading - 1 ) % 4
            turn = "L"
    except: pass
    try:
        if grid[coors_right[1]][coors_right[0]] == "#":
            new_heading = (heading + 1 ) % 4
            turn = "R"
    except: pass
    if new_heading is None: return []

    step = DIRS[new_heading]
    count = 0
    while 0 <= pos[0] + step[0] < width and 0 <= pos[1] + step[1] < height \
         and grid[pos[1]+step[1]][pos[0]+step[0]] == "#":
         pos = (pos[0] + step[0], pos[1] + step[1])
         count += 1
    
    return [f"{turn}{count}"] + get_path(grid, pos, new_heading)

def get_matches(haystack, needle):
    return [m.start() for m in re.finditer(needle, haystack)]

def extract_pattern(seq, others=[]):
    while any(seq[:len(other)] == other for other in others):
        for other_patt in others:
            len_other = len(other_patt)
            while seq[:len_other] == other_patt:
                seq = seq[len_other:]

    seq_str = ''.join(seq)

    for end in range(99):
        pattern = ''.join(seq[:end+1])
        matches = get_matches(seq_str[end+1:], pattern)

        if len(matches) < 2:
            break

    return seq[:end]


path = get_path(grid, robot_pos, robot_heading)

patt1 = extract_pattern(path)
patt2 = extract_pattern(path, [patt1])
patt3 = extract_pattern(path, [patt1, patt2])

path_str = ''.join(path)
pattern_strs = [''.join(patt) for patt in (patt1, patt2, patt3)]

for patt, letter in zip(pattern_strs, ("A", "B", "C")):
    path_str = re.sub(patt, letter, path_str)

robot_input = [ord(x) for x in ",".join(path_str) + "\n"]
for patt in (patt1, patt2, patt3):
    for elem in patt:
        m = re.match(r"(\w)(\d+)", elem)
        robot_input += [ord(m.group(1)), ord(",")]
        for num in m.group(2):
            robot_input.append(ord(num))
        robot_input.append(ord(","))
    robot_input = robot_input[:-1] + [ord("\n")]

robot_input += [ord("n"), ord("\n")]

code[0] = 2
comp = IntcodeComputer(code, robot_input)
print(comp.run())