import re
import math

regex = re.compile(r"x=(-?\d+), y=(-?\d+), z=(-?\d+)")

class Moon:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.speed = [0, 0, 0]

    def update_speed(self, moons):
        for moon in moons:
            for i in range(3):
                if self.pos[i] < moon.pos[i]:
                    self.speed[i] += 1
                elif self.pos[i] > moon.pos[i]:
                    self.speed[i] -= 1

    def kin_energy(self):
        return sum(abs(x) for x in self.speed)
    
    def pot_energy(self):
        return sum(abs(x) for x in self.pos)

    def total_energy(self):
        return self.kin_energy() * self.pot_energy()

    def step(self):
        self.pos = [self.pos[i] + self.speed[i] for i in range(3)]

    def __hash__(self):
        return hash(tuple(self.pos + self.speed))

moons = []
with open("input/day12.txt") as f:
    for line in f:
        m = regex.search(line)
        moons.append(Moon(int(m.group(1)), int(m.group(2)), int(m.group(3))))
N_MOONS = len(moons)

step = 0
states = [{} for _ in range(3)]
periods = [0 for _ in range(3)]

while True:

    for i in range(3):
        if periods[i]: continue
        state = hash((
            moons[0].pos[i], moons[0].speed[i],
            moons[1].pos[i], moons[1].speed[i],
            moons[2].pos[i], moons[2].speed[i],
            moons[3].pos[i], moons[3].speed[i],
        ))
        if state in states[i]:
            periods[i] = step
        else:
            states[i][state] = 0


    for i in range(N_MOONS):
        m = moons[i]
        others = moons[:i] + moons[i+1:]
        m.update_speed(others)
    [m.step() for m in moons]

    step += 1
    if step == 1000:
        print(sum(m.total_energy() for m in moons))

    if all(periods): break

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

lcm1 = lcm(periods[0], periods[1])
print(lcm(lcm1, periods[2]))