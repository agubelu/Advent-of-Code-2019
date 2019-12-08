WIDTH = 25
HEIGHT = 6

image = []
best = {0: 99999, 1: 0, 2: 0}

#### Parsing + Part 1
with open("input/day8.txt") as f:
    layer = []
    row = []
    count = {}

    for i, c in enumerate(f.read().strip(), start=1):
        digit = int(c)
        count[digit] = count.get(digit, 0) + 1

        row.append(digit)
        if i % WIDTH == 0:
            layer.append(row)
            row = []
        if (i / WIDTH) % HEIGHT == 0:
            image.append(layer)
            layer = []

            if count[0] < best[0]:
                best = count
            count = {}

print(best[1] * best[2])

#### Part 2
final_img = image[-1]
for i in range(len(image) - 2, 0, -1):
    layer = image[i]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel_img = final_img[y][x]
            pixel_layer = layer[y][x]
            final_img[y][x] = pixel_img if pixel_layer == 2 else pixel_layer

visual_img = [["■" if pixel == 1 else "□" for pixel in row] for row in final_img]
for row in visual_img:
    print(''.join(row))
