grid = {}
with open("input/day24.txt") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            grid[x, y] = char

dimensions = {0: grid.copy()}

#### Part 1
def count_bugs(x, y):
    coords = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
    return sum(1 for x_coord, y_coord in coords if grid.get((x_coord, y_coord), ".") == "#")

hashes = {hash(frozenset(grid.items())): 1}
while True:
    changes = {}

    for y in range(5):
        for x in range(5):
            cnt = count_bugs(x, y)
            if grid[x, y] == "#" and cnt != 1:
                changes[x, y] = "."
            elif grid[x, y] == "." and 1 <= cnt <= 2:
                changes[x, y] = "#"

    for (x, y), val in changes.items():
        grid[x, y] = val
    
    hsh = hash(frozenset(grid.items()))
    if hsh in hashes:
        break
    else:
        hashes[hsh] = 1

print(sum(2 ** i for i in range(25) if grid[i % 5, i // 5] == "#"))

#### Part 2
def get_dim(n):
    if n not in dimensions:
        dimensions[n] = {(x, y): "." for x in range(5) for y in range(5)}
    return dimensions[n]

# ugly but also beautiful in its own way :_)
def count_bugs_rec(x, y, n):
    coords = [(x, y-1, n), (x-1, y, n), (x+1, y, n), (x, y+1, n)]

    # Inner connections
    if (2,2,n) in coords:
        coords.remove((2,2,n))
    if (x,y) == (1,2):
        coords += [(0,j,n-1) for j in range(5)]
    if (x,y) == (2,1):
        coords += [(j,0,n-1) for j in range(5)]
    if (x,y) == (3,2):
        coords += [(4,j,n-1) for j in range(5)]
    if (x,y) == (2,3):
        coords += [(j,4,n-1) for j in range(5)]

    # Outer connections
    if any(i == -1 for i, _, _ in coords):
        coords += [(1,2,n+1)]
    if any(j == -1 for _, j, _ in coords):
        coords += [(2,1,n+1)]
    if any(i == 5 for i, _, _ in coords):
        coords += [(3,2,n+1)]
    if any(j == 5 for _, j, _ in coords):
        coords += [(2,3,n+1)]

    coords_remove = [(i,j,k) for i,j,k in coords if i in [-1,5] or j in [-1,5]]
    for elem in coords_remove: coords.remove(elem)
    coords = list(set(coords))
    return sum(1 for x_coord, y_coord, dim in coords if get_dim(dim)[x_coord, y_coord] == "#")

# Initialize one above and one below
get_dim(1)
get_dim(-1)
for _ in range(200):
    changes = {}

    dimensions_iterate = [d for d in dimensions]
    for dim in dimensions_iterate:
        for y in range(5):
            for x in range(5):
                if (x, y) == (2, 2): continue
                cnt = count_bugs_rec(x, y, dim)
                if get_dim(dim)[x, y] == "#" and cnt != 1:
                    changes[x, y, dim] = "."
                elif get_dim(dim)[x, y] == "." and 1 <= cnt <= 2:
                    changes[x, y, dim] = "#"

    for (x, y, dim), val in changes.items():
        get_dim(dim)[x, y] = val
    
print(sum(1 for x in range(5) for y in range(5) for dim in dimensions if dimensions[dim][x,y] == "#"))
