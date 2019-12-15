import re
from math import ceil

regex = re.compile(r"(\d+) (\w+)")

reactions = {}
with open("input/day14.txt") as f:
    for line in f:
        r, p = line.strip().split("=>")
        is_base = False
        m = regex.search(p)
        produce, quantity = m.group(2), int(m.group(1))
        react = []
        for x in r.split(","):
            m = regex.search(x)
            comp, amt = m.group(2), int(m.group(1))
            if comp == "ORE": is_base = True
            react.append((comp, amt))
        reactions[produce] = {'quantity': quantity, 'reaction': react, 'base': is_base}

def get_ore_cost(product, amount):
    leftovers = {}
    products = [(product, amount)]
    total = 0

    while not all(reactions[p[0]]['base'] for p in products):
        new_products = []
        for prod, amt in products:
            if reactions[prod]['base']:
                new_products.append((prod, amt))
                continue
            
            if leftovers.get(prod, 0) > 0:
                cons = min(amt, leftovers[prod])
                amt -= cons
                leftovers[prod] -= cons
            n_reacts = ceil(amt / reactions[prod]['quantity'])
            produced_quant = reactions[prod]['quantity'] * n_reacts
            leftovers[prod] = leftovers.get(prod, 0) + produced_quant - amt
            for prod2, amt2 in reactions[prod]['reaction']:
                new_products.append((prod2, amt2*n_reacts))

        d = {}
        for prod, amt in new_products:
            d[prod] = d.get(prod, 0) + amt
        products = list(d.items())

    for prod, amt in products:
        n_reacts = ceil(amt / reactions[prod]['quantity'])
        total += reactions[prod]['reaction'][0][1] * n_reacts
    return total

print(get_ore_cost('FUEL', 1))
MAX_ORE = 1e12
MIN_TRY = 100000
MAX_TRY = 100000000
last_try = 0
this_try = (MIN_TRY + MAX_TRY) // 2
best_ore = best_try = 0

while abs(last_try - this_try) > 1:
    ore = get_ore_cost('FUEL', this_try)
    if ore < MAX_ORE and ore > best_ore:
        best_try = this_try
    
    if ore < MAX_ORE:
        MIN_TRY = this_try
    else:
        MAX_TRY = this_try

    last_try = this_try
    this_try = (MIN_TRY + MAX_TRY) // 2

print(best_try)