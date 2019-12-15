from etc.intcode import from_file

comp = from_file("input/day13.txt")
blocks = 0

### Part 1:
while True:
    try:
        x, y, tile = comp.get_next_output(), comp.get_next_output(), comp.get_next_output()
        if tile == 2:  # Block
            blocks += 1
    except: break  # The computer raises an Exception when trying to get an input after it's done

print(blocks)

### Part 2:
comp = from_file("input/day13.txt")
comp.code[0] = 2
score = 0

ball_x = None
paddle_x = None

def get_joystick_input():
    if ball_x > paddle_x:
        return 1  # Move right
    elif ball_x < paddle_x:
        return -1  # Move left
    else:
        return 0  # Dont move

comp.set_inputs([get_joystick_input])

while True:
    try:
        x, y, tile = comp.get_next_output(), comp.get_next_output(), comp.get_next_output()
        if x == -1 and y == 0:
            score = tile
        elif tile == 3:  # Paddle
            paddle_x = x
        elif tile == 4:  # Ball
            ball_x = x
    except: break        

print(score)