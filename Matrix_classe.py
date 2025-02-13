import numpy as np
import  Determinantenfunctionen
import Variablen_bestimmen
import inspect
import customErrors
import matrix_arithmetic


class Matrix:
    def __init__(self, height:int, width:int, det_verfahren = 1, lgs_verfahren = 1, debug = False):
        if debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        # höhe = i breite = j
        if det_verfahren < 0 or det_verfahren > 1:
            raise ValueError("Das gewünschte Verfahren existiert nicht. Es gibt nut Verfahren von 0-1!")
        if det_verfahren < 0 or det_verfahren > 1:
            raise ValueError("Das gewünschte Verfahren existiert nicht. Es gibt nut Verfahren von 0-1!")
        if height < 2:
            raise ValueError("Die Matrix muss mindestens zwei Zeilen haben!")
        if width < 1:
            raise ValueError("Die Matrix muss mindestens eine Spalten haben!")
        self.height = height ; self.height_iter= height -1
        self.width = width ; self.width_iter = width-1
        self.array = np.zeros((height, width), dtype=np.float64)
        self.det_verfahren = det_verfahren # 0 wäre der Laplace Entwicklungssatz, 1 die LR_Zerlegung
        # ------------- verhindert das die determinante mehrmals berechnet wird -------------
        self.determinante = 0
        self.determinante_bestimmt = False
        # ------------- das muss anders gemacht werden------------# vielleicht eine weiter Klasse
        self.solution_vectors = {} # list[toggle if it was solved, solution, lr_matrix, solutions vector] <- lr_matrix is the matrix after "lrszerlegung" was applied with the sv
        # -------------- debug shit ---------------------
        self.debug = debug

    def __str__(self):
        return str(self.array)

    def __setitem__(self, index , value:float):
        # fertig
        """
            Diese funktion setzt den Wert an der gegebenen Stelle der Matrix auf den wert geg. in value
            :param index: position i und j in der Matrix
            :param value: wert zu welchem der Wert an der gegebenen position gesetzt werden soll
            :return: wert an der Stelle
        """
        if self.array.ndim == 1:
            self.array[index[0]] = value
        else:
            self.array[index] = value


    def __getitem__(self, index):
        # fertig
        """
            Diese funktion gibt den Wert an der gegebenen Stelle der Matrix zurück
            :param index: i und j in der Matrix
            :return: wert an der Stelle
        """
        if self.array.ndim == 1:
            return  self.array[index[0]]
        else:
            return self.array[index]

    def __mul__(self, matrix:'Matrix'):
        #fertig
        """
        Diese Funktion ermöglicht das Multiplizieren von Matrizen
            - Sind diese der Richtigen größe erfolgt eine normale multiplikative Verknüpfung zweier Matrizen
            - Sind diese beide in der Form gleich großer Vektoren, wird das Skalarprodukt errechnet
            - In jedem anderen Fall wird eine 0 zurückgegeben
        :param matrix: ein Objekt des Typs <Matrix>
        :return: neue Matrix / Skalar / error im Fall das die Objekte weder verknüpft noch via skalar multipliziert werden können
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        check = matrix_arithmetic.linking_or_skalar(self, matrix)
        if check == 1:
            return matrix_arithmetic.linking_of_matrix(self, matrix)
        elif check == 2:
            return matrix_arithmetic.skalar_of_matrix(self, matrix)
        else:
            raise ArithmeticError("Es konnte weder eine Verknüpfung noch Multiplikation ausgeführt werden.")

    def __add__(self, matrix:'Matrix'):
        """
        Diese Funktion ermöglicht, dass addieren von Matrizen.
        :param matrix: ein Objekt des Typs <Matrix>
        :return: neue Matrix mit erfolgter addition / error im Fall das die Matrizen ungleiche Dimensionen haben
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")

        result = matrix_arithmetic.addition(self, matrix)

        if result == 0:
            raise ArithmeticError("Es konnte leider keine Addition erfolgen, da die Dimensionen der Matrizen ungleich sind.")
        else:
            return result

    def __sub__(self, matrix:'Matrix'):
        """
        Diese Funktion ermöglicht, dass subtrahieren von Matrizen.
        :param matrix: ein Objekt des Typs <Matrix>
        :return: neue Matrix mit erfolgter subtraktion / error im Fall das die Matrizen ungleiche Dimensionen haben
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")

        result = matrix_arithmetic.subtraction(self, matrix)

        if result == 0:
            raise ArithmeticError("Es konnte leider keine Subtraktion erfolgen, da die Dimensionen der Matrizen ungleich sind.")
        else:
            return result

    def record_matrix(self):
        # fertig
        """
        Diese Funktion erfässt die Werte einer beliebigen Matrix und fügt sie der gegebenen Liste zum Speichern der Matrixwerte hinzu
        :return: 1 bei Erfolg
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        for i in range(self.height):
            for j in range(self.width):
                for attempt in range(10):
                    try:
                        get = float(input("a"+str(i+1)+str(j+1)+": "))
                    except ValueError:
                        print("Der Eingegebener Wert ist nicht valide!")
                    else:
                        break
                else:
                    print("Leider leider scheint es nicht möglich den richtigen Wert einzugeben. Lass uns von vorne beginnen.")
                    self.record_matrix()
                    return
                self.array[i, j] = get
        return 1

    def calculate_determinant(self):
        """
        Diese Funktion berechnet die Determinante der Matrix und gibt diese zurück
            -! falls die Determinante bereits berechnet wurde, wird diese einfach zurückgegeben
            -! wirft einen Fehler False keine Determinate bestimmt werden kann
        :return: determinante
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        if self.width != self.height:
            raise customErrors.DimensionError(f"Für diese Matrix kann keine Determinante bestimmt werden da Höhe und Breite ungleich sind \nHöhe: {self.height} \nBreite: {self.width}")
        # im Folgenden, wird nur die höhe abgefragt, da sie aufgrund der vorherigen abfrage
        # immer gleich der Breite sein muss
        if not self.determinante_bestimmt:
            if self.height == 2:
                Determinantenfunctionen.size_2x2(self)
            elif self.height == 3:
                Determinantenfunctionen.size_3x3(self)
            elif self.height > 3:
                if self.det_verfahren == 0:
                    Determinantenfunctionen.laplacescher_entwicklungssatz(self)
                elif self.det_verfahren == 1:
                    Determinantenfunctionen.lr_zerlegung(self)
                else:
                    raise customErrors.UndefindProcessError("Das verfahren existiert nicht!") #falls sich doch irgendwie ein falsches Verfahren durchgemogelt hat
            else:
                print(f"Ist die Matrix etwa der Größe 1x1, das ja frech. \nNaja dann ist die Determinant der Wert der Matrix selbst: {self.array[0, 0]}")
                self.determinante = self.array[0, 0]
                self.determinante_bestimmt = True
        return self.determinante

    def berechne_variablen(self, name, lgs_verfahren):
        # parameter vektor: Lösungsvektor der Größe nx0, wobei n gleich i der Matrix sein muss
        """
        Diese Funktion berechnet basierend auf einer gegebenen Matrix und einem gegebenen Lösungsvektor die Variablen
            -! falls diese bereits berechnet wurden, werden sie einfach zurückgegeben

        :return: 1 bei Erfolg, die Lösungswerte werden einfach in self.solutions hinterlegt
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")

        if name in self.solution_vectors.keys():
            if self.solution_vectors[name][0] and self.solution_vectors[name][3] == lgs_verfahren:
                print("FAILED")
                return 1
            else:
                # chose which process to use
                if self.solution_vectors[name][3] == 0:
                    Variablen_bestimmen.c_regel(self, name)
                elif self.solution_vectors[name][3] == 1:
                    Variablen_bestimmen.variablen_gaus_(self, name)
                return 1
        else:
            raise customErrors.ExistenceError("This solution vector does not exist.")

    def set_matrix(self, arr:np.array):
        """
        with this function the matrix can be set to a numpy array of any length or dimension
        :param arr: array to change to
        :return: nothing
        """
        self.array = arr.copy()

    def add_sv(self, name, lgs_verfahren, arr:np.array):
        """
        This function allows to add a new sv to the accumulation of solution vectors referenced to the matrix
        :param name: name of the solution vector
        :param lgs_verfahren: which lgs should be used to calculate variables in the future / 0 -> Laplace Entwicklungssatz, 1 -> die LR_Zerlegung
        :param arr: solutions vector as a np.array
        :return: nothing
        """
        if not name in self.solution_vectors.keys():
            self.solution_vectors.update({str(name) : [False, 0, 0, lgs_verfahren, arr.copy()]}) # list[toggle if it was solved, solution, lr_matrix, lgs_verfahren, solutions vector] <- lr_matrix is the matrix after "lrszerlegung" was applied with the sv

        # there is no else case, there is just nothing happening, for interacting with the interface that's easier

    def set_determinant(self, det):
        """
        This function is used to set a determinant
        :param det: which determinant that should be set
        :return: nothing
        """
        self.determinante = det
        self.determinante_bestimmt = True

    def return_matrix(self):
        """
        :return: a copy of the matrix values, numpy array
        """
        return self.array.copy()

    def return_lv(self, name):
        """
        returns a copy of a solution vector by a given name if it's in the solutions vector list of the Matrix
        :param name: name of a solution vector
        :return: copy of the solution vector
        """
        if name in self.solution_vectors.keys():
            return self.solution_vectors[name][-1].copy()
        else:
            raise customErrors.ExistenceError("This solution vector does not exist.")

    def get_height(self):
        """
        :return: height of the matrix
        """
        return self.height

    def get_width(self):
        """
        :return: width of the matrix
        """
        return self.width

    def get_solution(self, name):
        """
        returns a copy of the solution of a solution vector, given by the neame
        :param name: name of a solution vector
        :return: copy of the solution vector solution
        """
        if name in self.solution_vectors.keys():
            if self.solution_vectors[name][0]:
                return self.solution_vectors[name][1]
            else:
                raise customErrors.ExistenceError("The Variables have not been solved!")
        else:
            raise customErrors.ExistenceError("This solution vector does not exist.")

    def get_det(self):
        """
        :return: the determinant of the Matrix
        """
        if self.determinante_bestimmt:
            return self.determinante
        else:
            raise customErrors.ExistenceError("The Determinant has not been solved!")

    def set_det_process(self, verfahren):
        """
        Allows us to change/assign the det process used
        :param verfahren:
        :return:
        """
        if verfahren < 0 or verfahren > 1:
            raise ValueError("Das gewünschte Verfahren existiert nicht. Es gibt nut Verfahren von 0-1!")
        else:
            self.det_verfahren = verfahren

    def get_array_type(self):  # unused but may be helpful while debugging
        """
        :return: the type of the matrix array
        """
        return self.array.dtype
