class IntcodeComputer:

    def __init__(self, code, inputs=None):
        self.code = {i: val for i, val in enumerate(code)}
        self.inputs = inputs
        self.finished = False
        self.pointer = 0
        self.last_return = None
        self.rel_offset = 0

    def set_inputs(self, inputs):
        self.inputs = inputs

    def _ask_for_input(self):
        if type(self.inputs[0]) is int:
            return self.inputs.pop(0)
        else:
            return self.inputs[0]()

    def _process_cmd(self, pos):
        cmd = str(self.code.get(pos, 0))
        opcode = int(cmd[-2:])
        params = []

        if opcode in (1, 2, 7, 8):
            n_params = 3
        elif opcode in (5, 6):
            n_params = 2
        elif opcode in (3, 4, 9):
            n_params = 1
        else:
            n_params = 0

        while len(cmd) != 2+n_params:
            cmd = "0" + cmd
        
        for i in range(n_params):
            param_val = int(self.code.get(pos+1+i, 0))
            param_type = int(cmd[-3-i])
            param_mode = {
                0: 'POS',
                1: 'IMM',
                2: 'REL'
            }[param_type]
            params.append((param_val, param_mode))
        
        return {'op': opcode, 'params': params}

    def _get_param_val(self, param):
        if param[1] == "IMM":
            return param[0]
        elif param[1] == "POS":
            return self.code.get(param[0], 0)
        elif param[1] == "REL":
            return self.code.get(param[0] + self.rel_offset, 0)

    def _get_wr_addr(self, param):
        if param[1] == "POS":
            return param[0]
        elif param[1] == "REL":
            return param[0] + self.rel_offset

    def get_next_output(self):
        if self.finished:
            raise Exception("Trying to run a finished instance")

        while self.pointer in range(len(self.code)):
            data = self._process_cmd(self.pointer)
            opcode, params = data["op"], data["params"]

            # Ugly if-else thing
            if opcode in (1,2):
                # 1: Sum 2 values, 2: Multiply 2 values
                param1, param2, param3 = params[:3]
                val1 = self._get_param_val(param1)
                val2 = self._get_param_val(param2)
                wr_addr = self._get_wr_addr(param3)
                res = val1 + val2 if opcode == 1 else val1 * val2
                self.code[wr_addr] = res
            elif opcode == 3:
                # 3: Store an input value
                val = self._ask_for_input()
                pos = self._get_wr_addr(params[0])
                self.code[pos] = val
            elif opcode == 4:
                # 4: Output a value (in this case, return it)
                res = self._get_param_val(params[0])
                self.pointer += len(params) + 1
                self.last_return = res
                return res
            elif opcode in (5, 6):
                # 5: Jump to position if condition is not 0, 6: jump if 0
                cond = self._get_param_val(params[0])
                pos = self._get_param_val(params[1])
                if (opcode == 5 and cond != 0) or (opcode == 6 and cond == 0):
                    self.pointer = pos
                    continue
            elif opcode in (7, 8):
                # 7: Write 1 if parameter 1 < parameter 2, 0 otherwise
                # 8: Write 1 if parameter 1 = parameter 2, 0 otherwise
                param1, param2, param3 = params[:3]
                val1 = self._get_param_val(param1)
                val2 = self._get_param_val(param2)
                wr_addr = self._get_wr_addr(param3)
                res = 0
                if (opcode == 7 and val1 < val2) or (opcode == 8 and val1 == val2):
                    res = 1
                self.code[wr_addr] = res
            elif opcode == 9:
                # 9: Add a value to the relative offset
                val = self._get_param_val(params[0])
                self.rel_offset += val
            elif opcode == 99:
                # 99: Finish the execution
                break

            self.pointer += len(params) + 1

        self.finished = True
        return self.last_return

    def run(self):
        if self.finished:
            raise Exception("Trying to run a finished instance")
        while not self.finished:
            res = self.get_next_output()
        return res
