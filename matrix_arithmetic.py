from doctest import debug

import Matrix_classe
import inspect

def addition(matrix, matrix2):
    """
    TODO
    :param matrix:
    :param matrix2:
    :return: 0 ⇽ keine Operation möglich / 1 ⇽ Ergebnis
    """

    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")


    if matrix.height == matrix2.height and matrix.width == matrix2.width:
        new_matrix = Matrix_classe.Matrix(matrix.height, matrix.width, debug=matrix.debug)
        for i in matrix.height:
            for j in matrix.width:
                new_matrix[i][j] = matrix[i][j] + matrix2[i][j]

    return new_matrix



