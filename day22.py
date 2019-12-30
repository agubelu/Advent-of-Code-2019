import numpy as np

N_CARDS = 10007
moves = []

with open("input/day22.txt") as f:
    for line in f:
        line = line.strip()
        if line == "deal into new stack":
            moves.append(("NEW", 0))
        elif line.startswith("cut"):
            moves.append(("CUT", int(line[4:])))
        elif line.startswith("deal with increment"):
            moves.append(("INC", int(line[20:])))

def new_stack(stack, _):
    return np.flip(stack)

def cut_stack(stack, ind):
    return np.concatenate((stack[ind:], stack[:ind]))

def deal_increment(stack, inc):
    res = np.zeros(N_CARDS)
    for i in range(N_CARDS):
        res[i * inc % N_CARDS] = stack[i]
    return res 

movedict = {
    'NEW': new_stack,
    'CUT': cut_stack,
    'INC': deal_increment
}

#### Part 1
stack = np.arange(N_CARDS)
for move, data in moves:
    stack = movedict[move](stack, data)
print(np.where(stack == 2019)[0][0])

#### Part 2
N_CARDS = 119315717514047
REPS = 101741582076661  # bruh
POS = 2020

def new_stack_lin(a, b, data):
    return -a % N_CARDS, (N_CARDS - 1 - b) % N_CARDS

def cut_stack_lin(a, b, data):
    return a, (b - data) % N_CARDS

def deal_increment_lin(a, b, data):
    return (a * data) % N_CARDS, (b * data) % N_CARDS

movedict = {
    'NEW': new_stack_lin,
    'CUT': cut_stack_lin,
    'INC': deal_increment_lin
}

a = 1; b = 0
for move, data in moves:
    a, b = movedict[move](a, b, data)

r = (b * pow(1 - a, N_CARDS - 2, N_CARDS)) % N_CARDS
res = ((POS - r) * pow(a, REPS * (N_CARDS - 2), N_CARDS) + r) % N_CARDS
print(res)