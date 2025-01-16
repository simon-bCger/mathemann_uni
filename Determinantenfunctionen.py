import inspect
import  Matrix_classe
import numpy as np

import customErrors
from Variablen_bestimmen import variablen_gaus_


def size_2x2(matrix):
    # fertig
    """
    Diese Funktion berechnet die Determinante einer gegebenen 2x2 Matrix
    :param matrix: nimmt Matrix der Größe 2x2
    :return: Determinante
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    det = (matrix[0, 0]*matrix[1, 1])-(matrix[0, 1]*matrix[1, 0])
    matrix.set_determinant(det)
    return

def size_3x3(matrix): # regel von Sarrus
    # fertig
    """
    Diese Funktion berechnet die Determinante einer gegebenen 3x3 Matrix unter zuhilfenahme der Regel von Sarrus
    :param matrix: nimmt Matrix der Größe 3x3
    :return: Determinante
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    # Calculate the products of the diagonals from top-left to bottom-right
    v1 = matrix[0, 0] * matrix[1, 1] * matrix[2, 2]
    v2 = matrix[0, 1] * matrix[1, 2] * matrix[2, 0]
    v3 = matrix[0, 2] * matrix[1, 0] * matrix[2, 1]

    # Calculate the products of the diagonals from top-right to bottom-left
    v4 = matrix[0, 2] * matrix[1, 1] * matrix[2, 0]
    v5 = matrix[0, 0] * matrix[1, 2] * matrix[2, 1]
    v6 = matrix[0, 1] * matrix[1, 0] * matrix[2, 2]
    d = (v1+v2+v3)-(v4+v5+v6)
    matrix.set_determinant(d)
    return

def laplacescher_entwicklungssatz(matrix):
    # Fertig
    """
    Diese Funktion berechnet die Determinante einer Matrix beliebiger Größe
        - bei Größe 2x2 wird die Standard 2x2 Methode verwendet
        - bei Größe 3x3 wird die Regel von Sarrus verwendet
        - bei höheren Größen wird der laplacesche_entwicklungssatz angewendet
    Time complexity: O(!n) ⇽ bei optimaler Programmierung
    :param matrix: nimmt Matrix aller Größen
    :return: Determinante
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    # wir können hier davon ausgehen das nur matrizen der größe nxn n>0 an die Funktion gegeben wurden
    if matrix.height == 1:
        return matrix[0,0]
    elif matrix.height == 2:
        return size_2x2(matrix)
    elif matrix.height == 3:
        return size_3x3(matrix)
    else:
        return laplace_determinante(matrix)

def laplace_determinante(matrix):
    #fertig, außer Beschreibung
    """
    Diese Funktion berechnet die Determinante der Matrix, basierend auf dem Laplacian_Entwicklungssatz
    :param matrix: eine Matrix des typs 'Matrix'
    :return: die errechnete Determinante
    """
    # diese function wird sehr oft aufgerufen und printed deshalb nicht aus, wenn sie aufgerufen wird
    if matrix.height > 3:
        tu = beste_reihe_spalte_for_laplace(matrix)
        km = kleinere_matrix_geber(matrix, tu)
        accumulator = 0
        for i in range(len(km)):
            # bei gelöschter Zeile
            if tu[0] == 0:
                if matrix[tu[1],i] == 0:
                    accumulator += 0
                else:
                    v = laplace_determinante(km[i]) * matrix[tu[1],i]*((-1)**(tu[1]+i))
                    # print(f"v{i}: {v}")
                    accumulator += v
            # bei gelöschter Spalte
            else:
                if matrix[i,tu[1]] == 0:
                    accumulator += 0
                else:
                    v = laplace_determinante(km[i]) * matrix[i, tu[1]]*((-1)**(tu[1]+i))
                    # print(f"v{i}: {v}; first: {matrix[i, tu[1]]}; second: {((-1)**(tu[1]+i))} ")
                    accumulator += v
        matrix.set_determinant(accumulator)
    elif matrix.width == 3:
        size_3x3(matrix)
    else:
        size_2x2(matrix)
    return matrix.get_det()


def kleinere_matrix_geber(matrix, tu: tuple[int, int]):
    # fertig, beschreibung maybe überarbeiten
    """
    Diese Funktion berechnet alle kleineren Matrizen ab der Größe 3x3, aufwärts, basierend auf den Regeln des Laplaceschen Entwicklungssatzes
    :param tu: eine tuple, der erste wert gibt an, ob eine zeile oder spalte eliminiert wurde, der Zweite, welche es jeweils war eg. (1,2), spalte mit index 2, soll nicht genutzt werden
    :param matrix: nimmt Matrix ab der Größe 3x3
    :return: eine Liste aller kleineren Matrizen der nächsten kleineren Größe
    """
    # diese function wird sehr oft aufgerufen und printed deshalb nicht aus, wenn sie aufgerufen wird
    new_matrices = np.empty(int(matrix.height), dtype=Matrix_classe.Matrix)
    locations_main= np.empty(matrix.height*(matrix.height-1), dtype=tuple)
    c = 0
    # erstellen von arrays mit koordinaten welche für die neue Matrix infrage kommen,
    # wenn eine zeile "gelöscht" werden soll
    if tu[0] == 0:
        for i_fill in range(matrix.height):
            if i_fill != tu[1]:
                for j_fill in range(matrix.width):
                    locations_main[c] = (i_fill, j_fill)
                    c += 1
    # wenn eine spalte "gelöscht" werden soll
    elif tu[0] == 1:
        for i_fill in range(matrix.height):
            for j_fill in range(matrix.width):
                if j_fill != tu[1]:
                    locations_main[c] = (i_fill, j_fill)
                    c += 1

    # erstellen aller möglichen matrizen
    for j in range(matrix.width):
        locations_intern = np.empty((matrix.height-1)*(matrix.height-1), dtype=tuple)
        c = 0
        if tu[0] == 0:
            # wenn eine zeile "gelöscht" werden soll
            for ii in range(len(locations_main)):
                if locations_main[ii][1] != j:
                    locations_intern[c] = locations_main[ii]
                    c += 1
        else:
            # wenn eine spalte "gelöscht" werden soll
            for ii in range(len(locations_main)):
                if locations_main[ii][0] != j:
                    locations_intern[c] = locations_main[ii]
                    c += 1
        new_matrix = Matrix_classe.Matrix(matrix.height_iter, matrix.width_iter, det_verfahren=0)
        c = 0
        for i in range(matrix.height_iter):
            for jj in range(matrix.width_iter):
                new_matrix[i, jj] = matrix[locations_intern[c]]
                c += 1
        new_matrices[j] = new_matrix

    return new_matrices

def beste_reihe_spalte_for_laplace(matrix):
    # fertig
    """
    Diese Funktion findet die effizienteste Reihe oder Spalte um den Laplaceschen Entwicklungssatz anzuwenden
        → Die Reihe oder spalte mit den meisten Nullen
    :param matrix:
    :return: (0/1, number) → gibt '0' zurück, wenn es sich um eine Reihe handelt, 1 bei einer Spalte. 'number' steht für die betroffene Spalte oder Zeile
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    best = [0, 0]
    for i in range(matrix.height):
        a = 0
        a2 = 0
        for j in range(matrix.width):
            if matrix[i][j] == 0:
                a += 1
            if matrix[j][i] == 0:
                a2 *= 1
        if a > best[1]:
            best = [0, a]
        if a2 > best[1]:
            best = [1, a2]
    tu = (best[0], best[1])
    return tu


def gausssches_eliminationsverfahren(matrix):
    """
    Diese Funktion wendet das Gausssche Eliminationsverfahren an, um eine Stufenmatrix zu generieren,
    zudem erzeugt sie eine Matrix welche die Multiplikatoren für jede erzeugte Null enthält
    :param matrix:
    :return:
    basierend auf: https://de.wikipedia.org/wiki/Gau%C3%9Fsches_Eliminationsverfahren#LR-Zerlegung
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    lr_zerlegung(matrix, called_by_gaus=True)
    # print(f"Lr_Matrix: \n{matrix.return_lr_matrix(}")
    # print(f"solutions_vector_after_lr:\n{matrix.return_solutions_vector_after_lr()}")
    if matrix.determinante == 0:
        raise customErrors.DeterminantZeroError("Die Determinante der Matrix ist Null, folglich hat sie keine oder unendlich Lösungen!")
    else:
        # variablen lösungen errechnen
        variablen_gaus_(matrix)
    return

def lr_zerlegung(matrix, called_by_gaus = False):
    """
    Diese Funktion verwendet das lr_zerlegung-verfahren,
    dieses verwendet das gaußsche Eliminationsverfahren und multipliziert dann die Werte der Diagonalen
    zu den Werten L und U, welche multipliziert die Determinante der gegebenen Matrix ergibt.
    Time complexity: O(n^3) ⇽ bei optimaler Programmierung
    :param called_by_gaus: dieser, wird genutzt, falls die Funktion aus von der Funktion
                           "gausssches_eliminationsverfahren" aufgerufen wurde
    :param matrix: eine standard Matrix vom typ Matrix
    :return:
    shoutout:
        - https://www.youtube.com/watch?app=desktop&v=Th1EE-65u44&t=413s
        - https://de.wikipedia.org/wiki/Gau%C3%9Fsches_Eliminationsverfahren#LR-Zerlegung
    """
    if matrix.debug:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    custom_lv = Matrix_classe.Matrix # damit es weniger Warnungen gibt
    if called_by_gaus:
        custom_lv = Matrix_classe.Matrix(matrix.height, 1)
        custom_lv.set_matrix(matrix.return_lv())

    diagonal_matrix = Matrix_classe.Matrix(matrix.height, matrix.width)
    diagonal_matrix.set_matrix(matrix.return_matrix())
    # check:
    if diagonal_matrix[0, 0] == 0:
        for i in range(diagonal_matrix.height):
            if diagonal_matrix[i, 0] != 0:
                save = diagonal_matrix.array.copy()
                diagonal_matrix.array[0] = diagonal_matrix.array[i]
                diagonal_matrix.array[i] = save[0]
                break
        else:
            matrix.lr_matrix = diagonal_matrix
            return 0

    d = diagonal_matrix.array.diagonal()
    if 0 in d:  # diagonal produkt checken, wenn immer noch null, beenden!
        matrix.lr_matrix = diagonal_matrix
        return 0

    c = 1  # <- this counter lets us work thought the matrix in steps
    a = 1
    for j in range(matrix.width_iter):
        # print(diagonal_matrix)
        for i in range(c, matrix.height): # i beginnt bei 1 damit direkt in der zweiten Zeile begonnen wird
            check = diagonal_matrix[i][j]
            mult = 1 # einfach als neutrales element der Multiplikaton
            if check != 0:
                mult = (check / diagonal_matrix[c-1][j])  # nach der Formel (unten/oben)=multiplikator ; mit diesem x würde nach der Formel //unten-oben*multiplikator = 0// die aktuelle position in der Matrix 0 werden
            else:
                mult = 0 # so wird jede veränderung in dem Rest der Reihe nichtig da bei den folgenden Rechnunen immer die Zahl in der Zelle selbst als ergebnis kommt
            if j != matrix.width_iter or i != matrix.height_iter:
                diagonal_matrix[i, j] = 0

            for remaining_row in range(c, matrix.width):
                # print(f"calc: {diagonal_matrix[i][remaining_row]} - ({mult} * {diagonal_matrix[c-1][remaining_row]})")
                e = float(diagonal_matrix[i][remaining_row] - (mult * diagonal_matrix[c-1][remaining_row]))
                # print(f"e: {float(e)}, i: {i}, remaining_row: {remaining_row} at pos: {diagonal_matrix[i][remaining_row]}")
                # print("Will change:")
                # print(diagonal_matrix)
                diagonal_matrix[i, remaining_row] = float(e)
                # print("Changed!!")
                # print(diagonal_matrix)

            if called_by_gaus:
                # für den LV
                # print(f"customLv[{i}, {0}] = {custom_lv[i, 0]} - {mult} * {custom_lv[c - 1, 0]}")
                custom_lv[i, 0] = float(custom_lv[i, 0] - (mult * custom_lv[c - 1, 0]))


        a *= diagonal_matrix[c - 1][j]
        c += 1

    a *= diagonal_matrix[diagonal_matrix.height - 1, diagonal_matrix.width - 1]
    # print(f"Stufenform: \n {diagonal_matrix}")


    if called_by_gaus:
        matrix.set_lr(diagonal_matrix)
        matrix.lr_done = True
        matrix.set_determinant(round(a, 2))
        matrix.determinante_bestimmt = True
        matrix.set_solution_vector_after_lr(custom_lv)
        matrix.solution_vector_after_lr_done = True
        return
    # print(a)
    matrix.set_determinant(round(a, 2))
    return


