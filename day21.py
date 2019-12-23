from etc import intcode
from itertools import chain

comp = intcode.from_file("input/day21.txt")

def line_to_ascii(line):
    return [ord(char) for char in line + "\n"]

def print_comp(comp):
    while True:
        try:
            x = comp.get_next_output()
            if x > 255:
                print(x)
                break
            print(chr(x), end="")
        except: pass

commands = [
    "NOT A T",
    "OR T J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "WALK"]
comp.set_inputs(list(chain(*[line_to_ascii(line) for line in commands])))
print_comp(comp)

#### Part 2
comp = intcode.from_file("input/day21.txt")
commands = [
    "NOT A T",
    "OR T J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
    "RUN"]
comp.set_inputs(list(chain(*[line_to_ascii(line) for line in commands])))
print_comp(comp)