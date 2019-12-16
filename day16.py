import numpy as np

N_ITERS = 100
BASE_PATTERN = np.array([1, 0, -1, 0])

data = open("input/day16.txt").read().strip()
offset = int(data[:7])
ints = [int(x) for x in data]
data = np.array(ints)
len_data = len(data)

#### Part 1
# Build the pattern matrix
pattern = np.zeros((len_data, len_data))
for i in range(len_data):
    zeros = np.zeros(i)
    patt = np.repeat(BASE_PATTERN, i+1)
    patt = np.resize(np.array(patt), len_data - i)
    pattern[:,i] = np.concatenate((zeros, patt))

# Compute stuff
for i in range(N_ITERS):
    data = np.abs(data @ pattern) % 10

print(''.join(str(int(x)) for x in data[:8]))

#### Part 2
bigints = np.array(ints)
data = np.tile(bigints, 10000)[offset:]
for n in range(N_ITERS):
    data = np.abs(np.flip(np.cumsum(np.flip(data)))) % 10

print(''.join(str(int(x)) for x in data[:8]))
