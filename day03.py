def get_data(data):
    dirs = data.strip().split(",")
    res = []
    last = (0,0)

    for d in dirs:
        direct = d[0]
        num = int(d[1:])
        new = {
            'R': (last[0] + num, last[1]),
            'L': (last[0] - num, last[1]),
            'U': (last[0], last[1] + num),
            'D': (last[0], last[1] - num)
        }[direct]
        res.append([last, new])
        last = new
    
    return res

def check_inter(starthor, endhor, startver, endver):
    if starthor[0] < endhor[0]:
        rangex_hor = range(starthor[0], endhor[0] + 1)
    else:
        rangex_hor = range(endhor[0], starthor[0] + 1)
    y_hor = starthor[1]

    if startver[1] < endver[1]:
        rangey_ver = range(startver[1], endver[1] + 1)
    else:
        rangey_ver = range(endver[1], startver[1] + 1)
    x_ver = startver[0]

    if x_ver in rangex_hor and y_hor in rangey_ver:
        return (x_ver, y_hor)
    else:
        return None
    

def check_segments_intersect(seg1, seg2):
    start1, end1 = seg1
    start2, end2 = seg2

    if start1[0] == end1[0]:
        # seg1 vertical
        if start2[0] == end2[0]: 
            # seg2 vertical
            return None
        else:
            # seg2 horizontal
            return check_inter(start2, end2, start1, end1)

    elif start1[1] == end1[1]:
        # seg1 horizontal
        if start2[1] == end2[1]:
            # seg2 horizontal
            return None
        else:
            # seg2 vertical
            return check_inter(start1, end1, start2, end2)

    else:
        # ???
        raise Exception(f"{seg1} {seg2}")


with open("input/day3.txt") as f:
    line1, line2 = f.readlines()[:2]

d1 = get_data(line1)
d2 = get_data(line2)

intersections = []

for seg1 in d1:
    for seg2 in d2:
        res = check_segments_intersect(seg1, seg2)
        if res is not None and res != (0,0):
            intersections.append(res)

#distances = [abs(x[0]) + abs(x[1]) for x in intersections]
#print(min(distances))

############# Part 2

def distance_to_inter(line, point):
    dirs = line.strip().split(",")
    count = 0
    current = (0, 0)

    for d in dirs:
        direct = d[0]
        num = int(d[1:])
        step = {
            'R': (1, 0),
            'L': (-1, 0),
            'U': (0, 1),
            'D': (0, -1)
        }[direct]

        for _ in range(num):
            count += 1
            current = (current[0] + step[0], current[1] + step[1])
            if current == point:
                return count

inter_steps = [distance_to_inter(line1, p) + distance_to_inter(line2, p) for p in intersections]
print(min(inter_steps))
