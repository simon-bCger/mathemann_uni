from random import uniform, randint
import inspect
import numpy as np
import Matrix_classe


def random_matrix(width, height, lowest_value=0, highest_value=10, debug_mode=False):
    """
    This function creates a fully, randomly, filled Matrix based on the given Parameters. \n
    ! if lowest_value > highest_value they will switch such that: lowest_value = highest_value, highest_value = lowest_value
    :param width: the width of the matrix to create, should be > 0
    :param height: the height of the matrix to create, should be > 0
    :param lowest_value: the lowest value which should appear in the Matrix
    :param highest_value: the highest value which should appear in the Matrix
    :param debug_mode: as everywhere, if debug should happen or not
    :return: returns a fully filled Matrix with random numbers based on the Parameters
    """

    if lowest_value > highest_value:
        lowest_value, highest_value = highest_value, lowest_value

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    matrix = Matrix_classe.Matrix(height, width, debug=debug_mode)

    if not lowest_value.is_integer() or not highest_value.is_integer():
        for i in range(height):
            for j in range(width):
                matrix[i][j] = round(uniform(lowest_value, highest_value), 2)
    else:
        for i in range(height):
            for j in range(width):
                matrix[i][j] = randint(int(lowest_value), int(highest_value))

    return matrix

"""
def random_lv(matrix, s):
    a = np.zeros(s)
    for i in range(s):
        a[i] = randint(0, 5)
    matrix.set_sv(a)
"""
