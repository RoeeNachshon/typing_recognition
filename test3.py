import numpy as np
y = np.array([1, 2, 2, 2, 2, 0, 2, 3, 3, 3, 0, 0, 2, 2, 0])

print(np.count_nonzero(y == 1))

print(np.count_nonzero(y == 2))

print(np.count_nonzero(y == 3))
