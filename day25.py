from etc import intcode
import re
from copy import deepcopy
import sys
from itertools import chain, combinations

re_name = re.compile("== (.*) ==")
re_code = re.compile("typing (.*) on the keypad")
comp = intcode.from_file("input/day25.txt")

OPPOSITE_STEPS = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east', None: None}
rooms, items = {}, {}
FORBIDDEN_ITEMS = [ # These were determined by trial and error
    "photons",  # crashes the computer
    "giant electromagnet", # can't move!
    "escape pod",  # it escapes
    "molten lava",  # rip robot
    "infinite loop",  # yeah
]

global current_room
current_room = "Hull Breach"

def line_to_ascii(line):
    return [ord(char) for char in line + "\n"]

def give_command(comp, cmd):
    comp.set_inputs(line_to_ascii(cmd))

def get_next_text(comp):
    text = ""
    while True:
        try:
            char = comp.get_next_output()
            text += chr(char)
            if text.endswith("Command?\n"):
                break
        except: break  # The robot has finished
    return text

def get_room_info(text):
    m = re_name.search(text)
    title = m.group(1) if m else None
    directions = []
    items = []
    matching_dirs = matching_items = False
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            matching_dirs = matching_items = False
        elif line == "Doors here lead:":
            matching_dirs = True
        elif line == "Items here:":
            matching_items = True

        if (matching_dirs or matching_items) and line[0] == "-":
            item = line[2:]
            ls = directions if matching_dirs else items
            ls.append(item)

    return {'title': title, 'dirs': directions, 'items': items}

def dfs(previous_dir=None, previous_room=None):
    current_room_info = get_room_info(get_next_text(comp))
    title = current_room_info["title"]

    if title not in rooms:
        rooms[title] = deepcopy(current_room_info)
        del rooms[title]["title"]
        room_items = current_room_info["items"]
        if room_items and room_items[0] not in FORBIDDEN_ITEMS:
            items[room_items[0]] = title

    if previous_room:
        rooms[previous_room]["connects_to"] = rooms[previous_room].get("connects_to", []) + [(title, previous_dir)]
        rooms[title]["connects_to"] = rooms[title].get("connects_to", []) + [(previous_room, OPPOSITE_STEPS[previous_dir])]

    dirs = current_room_info['dirs']
    if previous_dir:
        dirs.remove(OPPOSITE_STEPS[previous_dir])
    
    if current_room_info['title'] == "Security Checkpoint":
        rooms[title]['control_dir'] = dirs[0]
        dirs = []

    for direction in dirs:
        give_command(comp, direction)
        dfs(direction, title)
        give_command(comp, OPPOSITE_STEPS[direction])
        get_next_text(comp)

if "--interactive" in sys.argv:
    while True:
        txt = get_next_text(comp)
        print(txt)
        cmd = input()
        give_command(comp, cmd)


# Explore the map
dfs()

def get_path(from_room, to_room):
    if from_room == to_room: return []
    paths = [[x] for x in rooms[from_room]["connects_to"]]
    while not any(path[-1][0] == to_room for path in paths):
        new_paths = []
        for path in paths:
            last_room = path[-1][0]
            connections = rooms[last_room]["connects_to"]
            for connect in connections:
                connect_name = connect[0]
                if len(path) < 2 or path[-2][0] != connect_name:
                    new_paths.append(path + [connect])
        paths = new_paths
    
    for path in paths:
        if path[-1][0] == to_room:
            return path

def move_to_room(dest_room):
    global current_room
    path = get_path(current_room, dest_room)
    for _, direction in path:
        give_command(comp, direction)
        get_next_text(comp)
    current_room = dest_room

def _take(item_name, drop=False):
    cmd = f"{'drop' if drop else 'take'} {item_name}"
    give_command(comp, cmd)
    get_next_text(comp)

def _drop(item_name): _take(item_name, drop=True)

def pickup_item(item_name, drop=False):
    item_room = items[item_name]
    move_to_room(item_room)
    if drop: _drop(item_name)
    else: _take(item_name)

def drop_item(item_name): pickup_item(item_name, drop=True)


### Try all possible item combinations
overweight_combinations = []
def powerset(ls):
    return chain.from_iterable(combinations(ls,n) for n in range(1, len(ls)+1))

def try_access_with_item_combo(combo):
    for item_name in combo:
        pickup_item(item_name)
    move_to_room("Security Checkpoint")
    access_dir = rooms["Security Checkpoint"]["control_dir"]
    give_command(comp, access_dir)
    text = get_next_text(comp)
    
    m = re_code.search(text)
    if m:
        return m.group(1)
    elif "are lighter than" in text:
        overweight_combinations.append(set(combo))

    for item_name in combo:
        drop_item(item_name)

combos = powerset(list(items))
print("Trying item combinations...")
for combo in combos:
    combo = set(combo)
    if any(x.issubset(combo) for x in overweight_combinations):
        continue
    code = try_access_with_item_combo(combo)
    if code:
        print(code)
        break



    