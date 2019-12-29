import itertools

class Planet:

    def __init__(self, name):
        self.name = name
        self.orbits = None
        self.orbited_by = []
    
    def set_orbits(self, planet):
        self.orbits = planet

    def get_orbits(self):
        return self.orbits

    def add_orbited_by(self, planet):
        self.orbited_by.append(planet)

    def get_orbited_by(self):
        return self.orbited_by

with open("input/day6.txt") as f:
    pairs = [line.strip().split(")") for line in f.readlines()]
    planets = set(itertools.chain(*pairs))
    planets_dict = {name: Planet(name) for name in planets}

    for p1, p2 in pairs:
        planets_dict[p2].set_orbits(planets_dict[p1])
        planets_dict[p1].add_orbited_by(planets_dict[p2])

total_orbits = 0
for planet in planets_dict.values():
    if planet.name == "COM": continue

    total_orbits += 1
    while planet.get_orbits().name != "COM":
        planet = planet.get_orbits()
        total_orbits += 1

print(total_orbits)

###### Part 2

start = planets_dict["YOU"].get_orbits()
target = planets_dict["SAN"].get_orbits()

visited = [start]
steps = 0

while target not in visited:
    steps += 1
    cands = [[x.get_orbits()] + x.get_orbited_by() for x in visited]
    cands = [x for x in list(itertools.chain(*cands)) if x is not None]
    cands = [x for x in cands if x not in visited]
    visited += cands

print(steps)