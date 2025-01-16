import numpy as np
import  Determinantenfunctionen
import Variablen_bestimmen
import matrix_multiplikation
import inspect
import customErrors


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
        self.lgs_verfahren = lgs_verfahren # 0 für cramersche Regel, 1 für Gaussalgorithmus
        self.lv = np.zeros((self.height, 1)) # erstellt einen LV gefüllt mit nullen
        self.solutions = np.zeros((self.height, 1)) # erstellt einen Array gefüllt mit nullen welche mit den errechneten Lösungen ersetzt werden können
        self.solved = False # Gibt an, ob schon die Variablen basierend auf dem LV berechnet wurden
        # ------------- absichern und checken, ob die lr_zerlegung schon angewendet wurde -------------
        self.lr_done = False
        self.lr_matrix = Matrix
        self.solution_vector_after_lr_done = False
        self.solution_vector_after_lr = Matrix
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
        check = matrix_multiplikation.linking_or_skalar(self, matrix)
        if check == 1:
            return matrix_multiplikation.linking_of_matrix(self, matrix)
        elif check == 2:
            return matrix_multiplikation.skalar_of_matrix(self, matrix)
        else:
            raise ArithmeticError("Es konnte weder eine Verknüpfung noch Multiplikation ausgeführt werden.")

    def __add__(self, matrix:'Matrix'):
        pass

    def __sub__(self, matrix:'Matrix'):
        pass

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

    def record_sv(self):
        # TODO fertig, beschreibung nötig
        """

        :return:
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        for i in range(self.height):
            for attempt in range(10):
                try:
                    get = float(input("x" + str(i + 1) + ": "))
                except ValueError:
                    print("Der Eingegebener Wert ist nicht valide!")
                else:
                    break
            else:
                print("Leider leider scheint es nicht möglich den richtigen Wert einzugeben. Lass uns von vorne beginnen.")
                self.record_sv()
                return
            self.lv[i] = get

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

    def berechne_variablen(self):
        # parameter vektor: Lösungsvektor der Größe nx0, wobei n gleich i der Matrix sein muss
        """
        Diese Funktion berechnet basierend auf einer gegebenen Matrix und einem gegebenen Lösungsvektor die Variablen
            -! falls diese bereits berechnet wurden, werden sie einfach zurückgegeben

        :return: 1 bei Erfolg, die Lösungswerte werden einfach in self.solutions hinterlegt
        """
        if self.debug:
            print(f"Executing: {inspect.currentframe().f_code.co_name}")
        if self.solved:
            return 1
        else:
            if self.lgs_verfahren == 0:
                Variablen_bestimmen.c_regel(self)
            elif self.lgs_verfahren == 1:
                Determinantenfunctionen.gausssches_eliminationsverfahren(self)
            return 1

    def set_matrix(self, arr:np.array):
        self.array = arr.copy()

    def set_sv(self, arr:np.array):
        self.lv = arr.copy()
        print(self.lv)

    def set_lr(self, matrix): # !be carefull, vectors of every length are possible, during calculation the needed numbers to match the size of the matrix will be substituted by zeros
        self.lr_matrix = matrix

    def set_determinant(self, det):
        self.determinante = det
        self.determinante_bestimmt = True

    def set_solution_vector_after_lr(self, solution_vector_after_lr):
        self.solution_vector_after_lr = solution_vector_after_lr

    def return_matrix(self):
        return self.array.copy()

    def return_lr_matrix(self):
        if self.lr_done:
            return self.lr_matrix.return_matrix(self)
        else:
            raise customErrors.ExistenceError("Es existiert keine lr_matrix, weshalb sie nicht zurück gegeben werden kann!")

    def return_solutions_vector_after_lr(self):
        if self.solution_vector_after_lr_done:
            return self.solution_vector_after_lr
        else:
            raise customErrors.ExistenceError("Es existiert kein solutions_vector_after_lr, weshalb dieser nicht zurück gegeben werden kann!")

    def return_lv(self):
        return self.lv.copy()

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_solutions(self):
        if self.solved:
            return self.solutions
        else:
            raise customErrors.ExistenceError("The Variables have not been solved!")

    def get_det(self):
        if self.determinante_bestimmt:
            return self.determinante
        else:
            raise customErrors.ExistenceError("The Determinant as not been solved!")

    def set_det_process(self, verfahren):
        if verfahren < 0 or verfahren > 1:
            raise ValueError("Das gewünschte Verfahren existiert nicht. Es gibt nut Verfahren von 0-1!")
        else:
            self.det_verfahren = verfahren

    def set_lgs_process(self, verfahren):
        if verfahren < 0 or verfahren > 1:
            raise ValueError("Das gewünschte Verfahren existiert nicht. Es gibt nut Verfahren von 0-1!")
        else:
            self.lgs_verfahren = verfahren

    def get_array_type(self):
        return self.array.dtype
