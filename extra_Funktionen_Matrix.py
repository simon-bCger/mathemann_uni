from random import randint

import numpy as np


def random_size(matrix, s):
    for i in range(s):
        for j in range(s):
            matrix[i][j] = randint(0, 5)

def random_lv(matrix, s):
    a = np.zeros(s)
    for i in range(s):
        a[i] = randint(0, 5)
    matrix.set_sv(a)


