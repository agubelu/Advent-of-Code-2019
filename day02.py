import sys

for input1 in range(0, 100):
    for input2 in range(0, 100):

        with open("input/day2.txt") as f:
            ls = [int(x) for x in f.read().strip().split(",")]

        ls[1] = input1
        ls[2] = input2

        i = 0
        while i in range(0, len(ls)):
            op = ls[i]
            if op == 99:
                break
            elif op in (1,2):
                pos1, pos2, pos3 = ls[i+1:i+4]
                a = ls[pos1]
                b = ls[pos2]
                if op == 1:
                    ls[pos3] = a + b
                else:
                    ls[pos3] = a * b
            else:
                raise Exception(f"Unknown opcode {op} at position {i}")
            i += 4

        res = ls[0]
        if res == 19690720:
            print(100 * input1 + input2)
            sys.exit(0)

