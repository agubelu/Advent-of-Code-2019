with open("input/day5.txt") as f:
    ls = [int(x) for x in f.read().strip().split(",")]

def process_cmd(ls, pos):
    cmd = str(ls[pos])
    opcode = int(cmd[-2:])
    params = []

    if opcode in (1, 2, 7, 8):
        n_params = 3
    elif opcode in (5, 6):
        n_params = 2
    elif opcode in (3, 4):
        n_params = 1
    else:
        n_params = 0

    while len(cmd) != 2+n_params:
        cmd = "0" + cmd
    
    for i in range(n_params):
        param_val = int(ls[pos + 1 + i])
        param_type = int(cmd[-3-i])
        param_mode = "POS" if param_type == 0 else "IMM"
        params.append((param_val, param_mode))
    
    return {'op': opcode, 'params': params}

def get_param_val(ls, param):
    if param[1] == "IMM":
        return param[0]
    elif param[1] == "POS":
        return ls[param[0]]

####
i = 0
while i in range(len(ls)):
    data = process_cmd(ls, i)
    opcode = data["op"]
    params = data["params"]

    # Ugly if-else thing
    if opcode in (1,2):
        param1, param2 = params[:2]
        val1 = get_param_val(ls, param1)
        val2 = get_param_val(ls, param2)
        res = val1 + val2 if opcode == 1 else val1 * val2
        ls[params[2][0]] = res
    elif opcode == 3:
        val = int(input("Input: "))
        pos = params[0][0]
        ls[pos] = val
    elif opcode == 4:
        val = get_param_val(ls, params[0])
        print(val)
    elif opcode in (5, 6):
        cond = get_param_val(ls, params[0])
        pos = get_param_val(ls, params[1])
        if (opcode == 5 and cond != 0) or (opcode == 6 and cond == 0):
            i = pos
            continue
    elif opcode in (7, 8):
        param1, param2 = params[:2]
        val1 = get_param_val(ls, param1)
        val2 = get_param_val(ls, param2)
        res = 0
        if (opcode == 7 and val1 < val2) or (opcode == 8 and val1 == val2):
            res = 1
        ls[params[2][0]] = res
    elif opcode == 99:
        break

    i += len(params) + 1

