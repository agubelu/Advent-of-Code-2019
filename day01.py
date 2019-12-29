with open("input/day1.txt") as f:
    fuel_list = [int(x.strip()) for x in f.readlines()]

def get_fuel_required(x):
    res = (x // 3) - 2
    return max(res, 0)

# Solution to part 1
print(sum(get_fuel_required(x) for x in fuel_list))

# Solution to part 2
total = 0
for fuel in fuel_list:
    while fuel > 0:
        fuel = get_fuel_required(fuel)
        total += fuel
print(total)