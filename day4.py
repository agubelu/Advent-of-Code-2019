START = 153517
END = 630395
rng = range(START, END+1)

def is_valid(n):
    adj_found = False
    n_str = str(n)

    for i in range(5):
        d1 = int(n_str[i])
        d2 = int(n_str[i+1])
        if d2 < d1:
            return False
        if d1 == d2:
            adj_found = True
    
    return adj_found

valid_pwds = [x for x in rng if is_valid(x)]
print(len(valid_pwds))

# Part 2
def is_valid_v2(n):
    adj_found = False
    n_str = str(n)

    for i in range(5):
        d1 = int(n_str[i])
        d2 = int(n_str[i+1])
        if d2 < d1:
            return False
        if d1 == d2:
            d3 = d4 = None

            try:
                d3 = int(n_str[i+2])
            except IndexError: pass
            try:
                d4 = int(n_str[i-1])
            except IndexError: pass

            if d3 == d1 or d4 == d1:
                continue

            adj_found = True
    
    return adj_found

valid_pwds_2 = [x for x in rng if is_valid_v2(x)]
print(len(valid_pwds_2))