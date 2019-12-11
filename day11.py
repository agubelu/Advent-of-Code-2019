from etc.intcode import IntcodeComputer

with open("input/day11.txt") as f:
    code = [int(x) for x in f.read().strip().split(",")]

def paint(start_color):
    comp = IntcodeComputer(code.copy())
    floor = {}
    pos = (0, 0)
    step_index = 0
    steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, right, down, left

    comp.set_inputs([start_color])
    while True:
        paint_color = comp.get_next_output()
        floor[pos] = paint_color
        if comp.finished: break
        rotation = comp.get_next_output()
        step_index += 1 if rotation == 1 else -1
        step = steps[step_index % 4]
        pos = (pos[0] + step[0], pos[1] + step[1])
        comp.set_inputs([floor.get(pos, 0)])

    return floor

#### Part 1
floor = paint(0)
print(len(floor))

#### Part 2
floor = paint(1)

MAX_X = MAX_Y = MIN_X = MIN_Y = 0
for x, y in floor.keys():
    if x > MAX_X: MAX_X = x
    elif x < MIN_X: MIN_X = x
    if y > MAX_Y: MAX_Y = y
    elif y < MIN_Y: MIN_Y = y

image = [["█" if floor.get((x,y), 0) else "░" for x in range(MIN_X, MAX_X + 1)] for y in range(MAX_Y, MIN_Y - 1, -1)]
for row in image:
    print(''.join(row))
