from intcode import IntcodeComputer
import turtle
import time

FACTOR = 10

with open("input/day11.txt") as f:
    code = [int(x) for x in f.read().strip().split(",")]

turtle = turtle.Turtle()
turtle.penup()
turtle.speed(75)
turtle.left(90)

comp = IntcodeComputer(code)
floor = {turtle.pos(): 1}

def paint_square(turtle, color):
    turtle.pendown()
    turtle.fillcolor("white" if color else "black")
    turtle.begin_fill()

    h = turtle.heading()
    turtle.setheading(0)
    for _ in range(4):
        turtle.forward(FACTOR)
        turtle.right(90)

    turtle.setheading(h)

    turtle.end_fill()
    turtle.penup()

while True:
    comp.set_inputs([floor.get((turtle.xcor() / FACTOR, turtle.ycor() / FACTOR), 0)])
    paint_color = comp.get_next_output()
    paint_square(turtle, paint_color)
    floor[(turtle.xcor() / FACTOR, turtle.ycor() / FACTOR)] = paint_color
    if comp.finished: break

    rotation = comp.get_next_output()
    if rotation == 1:
        turtle.right(90)
    else:
        turtle.left(90)
    turtle.forward(FACTOR)

time.sleep(10)