from etc.intcode import IntcodeComputer

grid = {}
code = [int(x) for x in open("input/day19.txt").read().strip().split(",")]

def try_coord(x,y):
    if (x,y) in grid: return grid[x,y]

    comp = IntcodeComputer(code.copy())
    comp.set_inputs([x, y])
    res = comp.get_next_output()

    grid[x,y] = res
    return res

def get_next(x, y):
    while try_coord(x, y+1): x += 1
    return x-1, y+1

#### Part 1
for y in range(50):
    on = False
    for x in range(50):
        val = try_coord(x,y)
        grid[x,y] = val
        if not on and val: on = True
        if on and not val: break

print(sum(grid.values()))

#### Part 2
x = max(i for i in range(50) if grid.get((i, 49), 0))
y = 49

while True:
    x, y = get_next(x, y)
    if x < 100 or y < 100: continue
    coords = [(x,y), (x-99,y), (x,y+99), (x-99,y+99)]
    if all(try_coord(i, j) for i, j in coords):
        print((x-99) * 10000 + y)
        break