from itertools import permutations 
import os

class IntcodeComputer:

    def __init__(self, code, inputs=None):
        self.code = code
        self.inputs = inputs
        self.finished = False
        self.pointer = 0
        self.last_return = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def _ask_for_input(self):
        if type(self.inputs[0]) is int:
            return self.inputs.pop(0)
        else:
            return self.inputs[0]()

    def _process_cmd(self, pos):
        cmd = str(self.code[pos])
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
            param_val = int(self.code[pos + 1 + i])
            param_type = int(cmd[-3-i])
            param_mode = "POS" if param_type == 0 else "IMM"
            params.append((param_val, param_mode))
        
        return {'op': opcode, 'params': params}

    def _get_param_val(self, param):
        if param[1] == "IMM":
            return param[0]
        elif param[1] == "POS":
            return self.code[param[0]]

    def get_next_output(self):
        while self.pointer in range(len(self.code)):
            data = self._process_cmd(self.pointer)
            opcode, params = data["op"], data["params"]

            # Ugly if-else thing
            if opcode in (1,2):
                param1, param2 = params[:2]
                val1 = self._get_param_val(param1)
                val2 = self._get_param_val(param2)
                res = val1 + val2 if opcode == 1 else val1 * val2
                self.code[params[2][0]] = res
            elif opcode == 3:
                val = self._ask_for_input()
                pos = params[0][0]
                self.code[pos] = val
            elif opcode == 4:
                res = self._get_param_val(params[0])
                self.pointer += len(params) + 1
                self.last_return = res
                return res
            elif opcode in (5, 6):
                cond = self._get_param_val(params[0])
                pos = self._get_param_val(params[1])
                if (opcode == 5 and cond != 0) or (opcode == 6 and cond == 0):
                    self.pointer = pos
                    continue
            elif opcode in (7, 8):
                param1, param2 = params[:2]
                val1 = self._get_param_val(param1)
                val2 = self._get_param_val(param2)
                res = 0
                if (opcode == 7 and val1 < val2) or (opcode == 8 and val1 == val2):
                    res = 1
                self.code[params[2][0]] = res
            elif opcode == 99:
                break

            self.pointer += len(params) + 1

        self.finished = True
        return self.last_return

### Part 1

with open("input/day7.txt") as f:
    code = [int(x) for x in f.read().strip().split(",")]

best_permutation = None
max_res = 0

for perm in permutations([0, 1, 2, 3, 4]):
    previous_output = 0

    for i in range(5):
        inputs = [perm[i], previous_output]
        computer = IntcodeComputer(code.copy(), inputs)

        while not computer.finished:
            previous_output = computer.get_next_output()

    if previous_output > max_res:
        max_res = previous_output
        best_permutation = perm

print(max_res, best_permutation)

#### Part 2
best_permutation = None
max_res = 0

for perm in permutations([5, 6, 7, 8, 9]):
    previous_output = 0

    comp1, comp2, comp3, comp4, comp5 = [IntcodeComputer(code.copy()) for _ in range(5)]

    comp1.set_inputs([perm[0], previous_output])
    comp2.set_inputs([perm[1], comp1.get_next_output])
    comp3.set_inputs([perm[2], comp2.get_next_output])
    comp4.set_inputs([perm[3], comp3.get_next_output])
    comp5.set_inputs([perm[4], comp4.get_next_output])

    while not comp5.finished:
        previous_output = comp5.get_next_output()
        comp1.set_inputs([previous_output])

    if previous_output > max_res:
        max_res = previous_output
        best_permutation = perm

print(max_res, best_permutation)