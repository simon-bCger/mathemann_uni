import Matrix_classe
import inspect
import numpy as np
import customErrors
import Determinantenfunctionen

def c_regel(matrix, name):
    """
    Diese Funktion wendet die Cramersche Regel an, um die Variablen der Matrix zu, bestimmen
    :param name: name of the solution vector we want to use
    :param matrix: matrix beliebiger größe nxn n>1
    :return: nichts
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    solution = np.zeros((matrix.height, 1))

    for j in range(matrix.width): # Die Breite muss den gleichen wert wie die Höhe des Lv sein, wir schlagen 2 Fliegen mit einer, klappe in dem wir über die Ursprungsmatrix gehen und jede spalte einmal ersetzten und dann den Wert an pos [j][0] in solutions einsetzten
        if not matrix.determinante_bestimmt:
            matrix.calculate_determinant()
        if matrix.determinante == 0:
            raise customErrors.DeterminantZeroError("Die Determinante der Matrix ist Null, folglich hat sie keine oder unendlich Lösungen!")
        new_matrix = Matrix_classe.Matrix(matrix.height, matrix.width, det_verfahren=1)
        new_matrix.set_matrix(matrix.return_matrix())
        #print(matrix.lv)
        for i in range(len(matrix.solution_vectors[name][-1])):
            new_matrix[i, j] = matrix.solution_vectors[name][-1][i]
            # print(matrix.solution_vectors[name][-1][i])
        new_matrix.calculate_determinant()

        solution[j] = round(new_matrix.determinante/matrix.determinante, 2)

    matrix.solution_vectors[name][0] = True
    matrix.solution_vectors[name][1] = solution.copy()

    return

def variablen_gaus_(matrix, name):
    """
    Diese Funktion errechnet die Variablen einer Matrize basierend auf der Stufenform
    der Matrize (workable), sowie des aus diesem folgenden Lösungsvektor(custom_lv)
    :param name: name of the solution vector we want to use
    :param matrix: matrix welche einer stufenform der selbigen enthält
    :return: nichts
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    if not matrix.determinante_bestimmt:
        matrix.calculate_determinant()

    if matrix.determinante == 0:
        raise customErrors.DeterminantZeroError("Die Determinante der Matrix ist Null, folglich hat sie keine oder unendlich Lösungen!")



    custom_lv = Determinantenfunctionen.lr_zerlegung(matrix, name=name, called_by_gaus=True)
    workable = matrix.solution_vectors[name][2].return_matrix() # Stufenform der Matrix
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

    matrix.solution_vectors[name][0] = True
    matrix.solution_vectors[name][1] = solutions.copy()

    return