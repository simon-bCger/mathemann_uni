from doctest import debug

import Matrix_classe
import inspect

def addition(matrix, matrix2):
    """
    this function adds two matrizes with the same dimensions together
    :param matrix: matrix to add
    :param matrix2: matrix to add
    :return: 0 ⇽ keine Operation möglich / Ergebnis
    """

    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")


    if matrix.height == matrix2.height and matrix.width == matrix2.width:
        new_matrix = Matrix_classe.Matrix(matrix.height, matrix.width, debug=matrix.debug)
        for i in range(matrix.height):
            for j in range(matrix.width):
                new_matrix[i][j] = matrix[i][j] + matrix2[i][j]

    return new_matrix


def subtraction(matrix, matrix2):
    """
    this function subtracts two matrizes with the same dimensions from each other
    :param matrix: matrix to subtract
    :param matrix2: matrix to subtract
    :return: 0 ⇽ keine Operation möglich / Ergebnis
    """

    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    if matrix.height == matrix2.height and matrix.width == matrix2.width:
        new_matrix = Matrix_classe.Matrix(matrix.height, matrix.width, debug=matrix.debug)
        for i in range(matrix.height):
            for j in range(matrix.width):
                new_matrix[i][j] = matrix[i][j] - matrix2[i][j]

    return new_matrix


#
# Im folgenden multiplikation
#


def linking_or_skalar(matrix, m2):
    """
    Diese Funktion checkt, ob eine der beiden operationen (verknüpfen oder Skalar berechnen) ausgeführt werden kann!
    :param matrix: Matrix 1
    :param m2: Matrix 2
    :return: 0 ⇽ keine Operation möglich / 1 ⇽ Verknüpfen / 2 ⇽ Skalar
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    # print(f"{matrix.get_height()}, { matrix.get_width()}, {m2.get_height()}, { m2.get_width()}")
    if matrix.get_width() == m2.get_height():
        return 1
    elif matrix.get_height() == m2.get_height() and matrix.get_width() == 1 and m2.get_width() == 1:
        return 2
    else:
        return 0

def skalar_of_matrix(matrix, v2):
    """
    Diese Funktion berechnet das Skalar zweier Vektoren, sie geht davon aus das beide multiplizierbar sind
    :return: Ergebnis
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    skalar = 0
    for i in range(matrix.get_height()):
        skalar += (matrix[i, 0] * v2[i, 0])
    return skalar

def linking_of_matrix(matrix, m2):
    """
    Diese Funktion verknüpft zwei Matrizen, sie geht davon aus das beide verknüpfbar sind
    :return: verknüpfte matrix
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    new_matrix = Matrix_classe.Matrix(matrix.get_height(), m2.get_width())

    # print(f"Matrix 1 height: {matrix.get_height()}; Matrix 1 width: {matrix.get_width()}; Matrix 2 height: {m2.get_height()}; Matrix 2 width: {m2.get_width()}")
    # print(f"NewMatrix ->\nwidth: {new_matrix.get_width()}\nheight: {new_matrix.get_height()}")

    for i in range(new_matrix.get_height()):
        for j in range(new_matrix.get_width()):
            skalar = 0
            for ii in range(m2.get_height()):
                # print(f"i: {i}, ii: {ii}")
                x = matrix[i, ii]
                y = m2[ii, j]
                # print(f"{x} * {y} =", end="")# print(f"x:{x}:{type(x)}, y:{y}:{type(y)}")
                x = float(x) * float(y)
                # print(x)
                skalar += x
            new_matrix[i, j] = skalar

    return new_matrix


