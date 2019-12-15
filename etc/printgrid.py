def print_grid():
    MAX_X = MAX_Y = MIN_X = MIN_Y = 0
    for x, y in tiles.keys():
        if x > MAX_X: MAX_X = x
        elif x < MIN_X: MIN_X = x
        if y > MAX_Y: MAX_Y = y
        elif y < MIN_Y: MIN_Y = y

    def valimg(x, y):
        try:
            val = tiles[(x,y)]
            if val == 0: return "█"
            elif val == 1: return "░"
            else: return "O"
        except: return "X"

    image = [[valimg(x,y)
              for x in range(MIN_X, MAX_X + 1)] for y in range(MAX_Y, MIN_Y - 1, -1)]
    for row in image:
        print(''.join(row))