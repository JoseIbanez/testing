size = 1000000

# High memory allocation
x = [i for i in range(size)]
y = [i for i in range(size)]

# High computation time
for i in range(size):
    y[i] = y[i] * y[i]


