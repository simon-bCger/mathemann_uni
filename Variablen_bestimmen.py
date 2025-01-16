import Matrix_classe
import inspect
import numpy as np
import customErrors

def c_regel(matrix):
    """
    Diese Funktion wendet die Cramersche Regel an, um die Variablen der Matrix zu, bestimmen
    :param matrix: matrix beliebiger größe nxn n>1
    :return: nichts
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    for j in range(matrix.width): # Die Breite muss den gleichen wert wie die Höhe des Lv sein, wir schlagen 2 Fliegen mit einer, klappe in dem wir über die Ursprungsmatrix gehen und jede spalte einmal ersetzten und dann den Wert an pos [j][0] in solutions einsetzten
        if not matrix.determinante_bestimmt:
            matrix.calculate_determinant()
        if matrix.determinante == 0:
            customErrors.DeterminantZeroError("Die Determinante der Matrix ist Null, folglich hat sie keine oder unendlich Lösungen!")
        new_matrix = Matrix_classe.Matrix(matrix.height, matrix.width, det_verfahren=1)
        new_matrix.set_matrix(matrix.return_matrix())
        #print(matrix.lv)
        for i in range(len(matrix.lv)):
            new_matrix[i, j] = matrix.lv[i]
            print(matrix.lv[i])
        new_matrix.calculate_determinant()
        matrix.solutions[j] = round(new_matrix.determinante/matrix.determinante, 2)
    matrix.solved = True
    return


def variablen_gaus_(matrix):
    """
    Diese Funktion errechnet die Variablen einer Matrize basierend auf der Stufenform
    der Matrize (workable), sowie des aus diesem folgenden Lösungsvektor(custom_lv)
    :param matrix: matrix welche einer stufenform der selbigen enthält
    :return: nichts
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    custom_lv = matrix.return_solutions_vector_after_lr()
    workable = matrix.lr_matrix.return_matrix() # Stufenform der Matrix
    solutions = np.zeros(custom_lv.height, dtype=float)

    for i in range(matrix.height-1, -1, -1):
        current_value = custom_lv[i, 0]
        counter=matrix.height-1
        #print(f"workable[i]: {workable[i]}")
        while True:
            # print(f"current_value: {current_value} \ncounter: {counter}\ncustom_lv:\n{custom_lv.return_matrix()}\nworkable:\n{workable}\ni: {i}\n")
            if np.count_nonzero(workable[i]) == 1 or np.count_nonzero(workable[i]) == 0: # ==0 ist für alle Matrizen welche nach Stufenform unten rechts eine null haben
                # print("break")
                break
            else:
                #print(f"i: {i} counter: {counter}, workable: \n{workable}")
                #print(f"{current_value} += {custom_lv[counter, 0]} * {workable[i, counter]}", end=" = ")
                e = custom_lv[counter, 0] * workable[i, counter]
                current_value -= e # wenn das ergebnis + ist muss es abgezogen werden, wenn - muss es addiert werden, durch -(-e) passiert genau das
                #print(e)
                workable[i, counter] = 0
                counter -= 1

        # print(f"{custom_lv[i, 0]} = {current_value} / {workable[i, i]} = {current_value/workable[i,i]}")
        custom_lv[i, 0] = current_value/workable[i, i]
        workable[i, counter] = 0
        solutions[i] = custom_lv[i, 0]
    matrix.solutions = solutions
    matrix.solved = True
    return