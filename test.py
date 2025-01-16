import numpy as np

class CustomArray:
    def __init__(self, shape):
        self.array = np.zeros(shape)

    def __setitem__(self, i, j, value):
        self.array[(i, j)] = value

    def __getitem__(self, key):
        return self.array[key]

# Usage
custom_array = CustomArray((3, 2))

# Setting values
custom_array[0][0] = 1
custom_array[1][1] = 2
custom_array[2][1] = 3

# Getting values
print(custom_array[0, 0])  # Output: 1.0
print(custom_array[1, 1])  # Output: 2.0
print(custom_array[2, 1])  # Output: 3.0

# Printing the entire array
print(custom_array.array)
