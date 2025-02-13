from os import system
import Matrix_classe
import numpy as np
from time import time_ns
import inspect
import extra_Funktionen_Matrix
import customErrors


def print_help_menu(debug_mode):
    """
    This function prints the help menu
    :param debug_mode: toggle for debugMode
    :return: nothing
    """
    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")
    print("<---- Help Menu ----->")
    print("help             enter this to print the help menu")
    print("exit             enter this to exit the current mode ore quit the programm as a whole")
    print("cls              enter this to clean the console")
    print("cleanMode        enter this to switch to or into cleanMode, which clears the console regularly")
    print("arithMode        enter this to enter the multiplikation mode")
    print("debugMode        enter this to toggle debugMode")
    print("det              enter this to determine the Determinant of a Matrix")
    print("v                enter this to determine the Variables based on the Matrix an Solutionvektor")
    print("new m            enter this to set or reset a Matrix")
    print("new sv           enter this to set or reset a Solutionvektor")
    print("current m/sv     enter this to display all the saved Matrizes or Solutionvektors")
    print("<-------------------->")

def check_arithmetic_operators(operator:str, matrix, matrizes, debug_mode):
    """
    This function checks which of the available matrizes can be calculated with the chosen matrix
    :param operator: takes a string, which is should be an arithmetic operator, else error
    :param matrix: die matrix welche geprüft werden soll
    :param matrizes: takes all matrizes
    :param debug_mode: toggle for debugMode
    :return: a list of keys of the possible Matrizes
    """

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    possible_matrizes = {}

    if operator == "+" or operator == "-": # they both have the same requirements
        for m_name in matrizes.keys():
            if matrizes[m_name].height == matrix.height and matrizes[m_name].width == matrix.width:
                possible_matrizes.update({str(m_name): matrizes[m_name]})

    elif operator == "*":
        for m_name in matrizes.keys():
            if ((matrix.width == matrizes[m_name].height) or
                (matrix.get_height() == matrizes[m_name].get_height() and matrix.get_width() == 1 and matrizes[m_name].get_width() == 1)):

                possible_matrizes.update({str(m_name): matrizes[m_name]})
                
    else:
        raise customErrors.SlipUpError("Somehow you chose an arithmetic_operator which is not existent or unaccounted for :(")

    return possible_matrizes

def arith_mode(matrizes, clean_mode, debug_mode):
    """
    This function lets you enter a continues arithmatic mode, where you can perform arithmetic
    operations on all existing Matrices
    :param matrizes: takes alle matrizes
    :param clean_mode: toggle for cleanMode
    :param debug_mode: toggle for debugMode
    :return: nothing
    """
    # works
    if clean_mode:
        system("cls")

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    # this is needed, else "dict_keys(...)" is printed and we only want (...)
    key_list = str(list(matrizes.keys()))
    key_list = key_list.replace("[", "")
    key_list = key_list.replace("]", "")

    while True: # sicher gehen das genug matrizes zum Rechnen vorhanden sind mind.(2)
        if len(matrizes) < 2:
            print(f"Leider stehen nicht genug Matrizen zur auswahl geg.[{len(matrizes)}], mind.[2]!")
            print(f"Möchtest du weitere Matrizen hinzufügen?")
            while True:
                get = input(f"y/n /> ")
                if get == "y":
                    matrizes = set_matrix(matrizes, clean_mode, debug_mode)
                    break
                elif get == "n":
                    return matrizes
                else:
                    print("Keine Valide Eingabe!")
        else:
            break

    while True: # ab hier kann so viel gerechnet werden wie gewünscht
        print("Führe eine Rechnung aus ->")
        while True:
            print(f"Alle möglichen Matrizen:\n{key_list}")
            m_name1 = input("Erste Matrix /> ")
            if m_name1 in matrizes.keys():
                break

            if m_name1 == "exit":
                return matrizes
            print("Matrix nicht vorhanden!")

        while True:
            valide_rechenzeichen = ["+", "-", "*"]
            print(f"Gib ein Valides Rechenzeichen an {valide_rechenzeichen} !")
            rechenzeichen = input("Rechenzeichen /> ")
            if rechenzeichen in valide_rechenzeichen:
                break
            if rechenzeichen == "exit":
                return matrizes
            print("Kein Valides Rechenzeichen!")

        while True:
            possible_m = check_arithmetic_operators(rechenzeichen, matrizes[m_name1], matrizes, debug_mode)

            # this is needed, else "dict_keys(...)" is printed and we only want (...)
            possible_m_keys = str(list(possible_m.keys()))
            possible_m_keys = possible_m_keys.replace("[", " ")
            possible_m_keys = possible_m_keys.replace("]", " ")

            if len(possible_m) > 0:
                print(f"Alle möglichen Matrizen:\n{possible_m_keys}")
                m_name2 = input("Zweite Matrix /> ")
                if m_name2 in possible_m.keys():
                    break
                if m_name2 == "exit":
                    return matrizes
                print("Matrix nicht vorhanden!")
            else:
                print("Leider gibt es keine Matrix mit welcher dein Rechenvorgang möglich ist!")
                print(f"Möchtest du weitere Matrizen hinzufügen?")
                while True:
                    get = input(f"y/n /> ")
                    if get == "y":
                        matrizes = set_matrix(matrizes, clean_mode, debug_mode)
                        break
                    elif get == "n":
                        return matrizes
                    else:
                        print("Keine Valide Eingabe!")

        if clean_mode:
            system("cls")

        print("<----------- Alte Rechnung ----------->")
        print(f"Es wird berechnet: {m_name1} {rechenzeichen} {m_name2}")
        # addition
        if rechenzeichen == "+":
            t = time_ns()
            try:
                e = matrizes[m_name1] + matrizes[m_name2]
            except ArithmeticError:
                print("Es konnte leider keine Addition erfolgen, da die Dimensionen der Matrizen ungleich sind!")
            else:
                print(f"Ergebnis: \n{e}")
                t2 = time_ns() - t
                print(f"Benötigte Zeit:\n Sekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}")
        # subtraktion
        elif rechenzeichen == "-":
            t = time_ns()
            try:
                e = matrizes[m_name1] - matrizes[m_name2]
            except ArithmeticError:
                print("Es konnte leider keine Addition erfolgen, da die Dimensionen der Matrizen ungleich sind!")
            else:
                print(f"Ergebnis: \n{e}")
                t2 = time_ns() - t
                print(
                    f"Benötigte Zeit:\n Sekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}")
        # multiplikation
        elif rechenzeichen == "*":
            t = time_ns()
            try:
                e = matrizes[m_name1] * matrizes[m_name2]
            except ArithmeticError:
                print("Es konnte weder eine Verknüpfung noch ein Skalar bestimmt werden!")
            else:
                print(f"Ergebnis: \n{e}")
                t2 = time_ns() - t
                print(f"Benötigte Zeit:\n Sekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}")
        else:
            raise customErrors.SlipUpError("Somehow you chose an arithmetic_operator which is not existent or unaccounted for :(")
        print("<----------- Neue Rechnung ----------->")

def calc_determinant(matrizes, clean_mode, debug_mode):
    """
    :param matrizes: takes all matrizes
    :param clean_mode: toggle for cleanMode
    :param debug_mode: toggle for debugMode
    :return: list of current matrizes
    """
    # works
    if clean_mode:
        system("cls")

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    all_possible_matrices = [] # damit die person nur Matrizen auswählen kann welche größe nxn haben
    for key in matrizes.keys():
        if matrizes[key].get_height() == matrizes[key].get_width():
            all_possible_matrices.append(key)

    while True:
        print(f"Alle möglichen Matrizen:\n{all_possible_matrices}")
        m_name = input("Matrix von welcher die Determinante bestimmt werden soll: ")
        if m_name in all_possible_matrices:
            break

        if m_name == "exit":
            return matrizes
        print("Matrix nicht vorhanden!")

    if matrizes[m_name].get_width() > 3: # falls die Matrix kleiner 4x4 ist, wird automatisch sarrus verwendet
        verfahren = 1
        while True:
            try:
                verfahren =int(input("Eingabe des Verfahrens (0:Laplace / 1:LR-Zerlegung): "))
            except ValueError:
                print("Keine Valide eingabe!")
            if verfahren == 0 or verfahren == 1:
                matrizes[m_name].set_det_process(verfahren)
                break
            else:
                print("Zahl nicht im Wertebereich!")

    t = time_ns()
    matrizes[m_name].calculate_determinant()
    t2 = time_ns() - t

    print(f"Determinante: {matrizes[m_name].get_det()}")
    print(f"Benötigte Zeit:\nSekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}")

    return matrizes

def calc_variables(matrizes, lvs, clean_mode, debug_mode):
    """
    This function lets you calculate the variables for a chosen matrix and a chosen solutionvector
    TODO Matizen lassen keine neuen LV zu, es wird einfach die Lösung mit dem alten LV angegeben!!! überarbeiten !!! geschafft brudi <3
    :param matrizes: takes all matrizes
    :param lvs: takes all solution vectors
    :param clean_mode: toggle for cleanMode
    :param debug_mode: toggle for debugMode
    :return: list of current matrizes
    """
    # works
    if clean_mode:
        system("cls")

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    all_possible_matrices = []  # damit die person nur Matrizen auswählen kann welche größe nxn haben
    for key in matrizes.keys():
        if matrizes[key].get_height() == matrizes[key].get_width():
            all_possible_matrices.append(key)

    while True:
        print(f"Alle möglichen Matrizen:\n{all_possible_matrices}")
        m_name = input("Matrix von welcher die Variablen bestimmt werden sollen: ")
        if m_name in all_possible_matrices:
            break
        if m_name == "exit":
            return matrizes
        print("Matrix nicht vorhanden!")

    while True:
        # get all keys with the right lenght
        possible_keys = []
        for key in lvs.keys():
            if lvs[key].get_height() == matrizes[m_name].get_height():
                possible_keys.append(key)
        if len(possible_keys) > 0:
            print(f"Alle möglichen Lösungsvektoren:\n{possible_keys}")
            l_name = input("LV zum bestimmen der Variablen: ")
            if l_name in lvs.keys():
                break
            if l_name == "exit":
                return matrizes
            print("Lösungsvektor nicht vorhanden!")
        else:
            while True:
                print("Leider gibt es keinen Vektor der zum lösen der Matrix in frage kommen würde.")
                print("Füge einen weiteren Vektor hinzu, indem du seinen namen eingibst, oder gib exit ein, um dieses Menü zu verlassen.")
                get = input("//> ")
                if get == "exit":
                    return matrizes
                set_solution_vector(lvs, clean_mode, debug_mode, pre_name=get)
                break

    while True:
        try:
            print("Wenn du ein anderes Verfahren nutzt als zuvor, wird mit diesem Verfahren neu berechnet.\nDies erlaubt zeitliche unterschiede zu berechnen :)")
            verfahren = int(input("Eingabe des Verfahrens (0:CramerscheRegel / 1:GaussschesEliminationsVerfahren): "))
        except ValueError:
            print("Keine Valide eingabe!")
        else:
            if verfahren == 0 or verfahren == 1:
                break
            else:
                print("Zahl nicht im Wertebereich!")

    # matrizes[m_name].set_lgs_process(verfahren)
    matrizes[m_name].add_sv(l_name, verfahren, lvs[l_name].return_matrix())

    #print(matrizes[m_name].solution_vectors)
    t = time_ns()
    try:
        matrizes[m_name].berechne_variablen(l_name, verfahren)
    except customErrors.DeterminantZeroError:
        t2 = time_ns() - t
        print("Es gibt leider keine oder unendlich viele Lösungen!")
        print(f"Benötigte Zeit:\nSekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}\n")
    else:
        t2 = time_ns() - t
        print(f"Benötigte Zeit:\nSekunden: {t2 * 10 ** (-9)}, Millisekunde: {t2 * 10 ** (-6)}, Mikrosekunde: {t2 * 10 ** (-3)}, Nanosekunde: {t2}")
        print(f"Lösung: {matrizes[m_name].get_solution(l_name)}")

    return matrizes

def set_matrix(matrizes, clean_mode, debug_mode):
    """
    This function lets you set new matrizes
    :param matrizes: takes all matrizes
    :param clean_mode: toggle for cleanMode
    :param debug_mode: toggle for debugMode
    :return: list of current matrizes
    """
    # works
    if clean_mode:
        system("cls")

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    m = Matrix_classe.Matrix(2, 2)  # just so my interpreter stops whining

    while True:
        name = input("Name der Matrix: ")

        if name == "exit":  # möglichkeit das unterprogramm zu verlassen, falls man sich vertan hat
            return matrizes

        if name in matrizes.keys():
            get = input("The Matrix already exists. Do you want to override it? [y/n]:")
            if get == "y":
                break
        else:
            break

    while True:
        try:
            zeilen = int(input("Anzahl der Zeilen: "))
        except ValueError:
            print("Keine Valide eingabe!")
        else:
            if zeilen > 1:
                break
            else:
                print("Zu wenig Zeilen!")

    while True:
        try:
            spalten = int(input("Anzahl der Spalten: "))
        except ValueError:
            print("Keine Valide eingabe!")
        else:
            if spalten > 0:
                break
            else:
                print("Zu wenig spalten!")

    while True:
        get = input("Soll die Matrix mit zufälligen Werten gefüllt werden? [y/n]:")

        if get == "y" or get == "yes":
            while True:
                try:
                    lowest_value = float(input("Gib den niedrigsten Wert ein welcher die Matrix beinhalten soll:"))
                except ValueError:
                    print("Keine Valide eingabe!")
                else:
                    break

            while True:
                try:
                    highest_value = float(input("Gib den höchsten Wert ein welcher die Matrix beinhalten soll:"))
                except ValueError:
                    print("Keine Valide eingabe!")
                else:
                    break


            m = extra_Funktionen_Matrix.random_matrix(spalten, zeilen, lowest_value, highest_value, debug_mode=debug_mode )
        elif get == "n" or get == "no":
            m = Matrix_classe.Matrix(zeilen, spalten, debug=debug_mode)
            m.record_matrix()
        else:
            print("Keine Valide eingabe!")

        break

    matrizes.update({name : m})
    print("Matrix erfolgreich erstellt")
    return matrizes

def set_solution_vector(lvs, clean_mode, debug_mode, pre_name="not_given"):
    """
    This function lets you set new solution vectors
    :param lvs: list of solution vectors
    :param clean_mode: toggle for cleanMode
    :param debug_mode: toggle for debugMode
    :param pre_name: weirdly I implemented this
    :return: list of solution vectors
    """
    #works
    if clean_mode:
        system("cls")

    if debug_mode:
        print(f"Executing: {inspect.currentframe().f_code.co_name}")

    while True:
        if pre_name == "not_given":
            name = input("Name des Vektors: ")
        else:
            name = pre_name

        if name == "exit":  # möglichkeit das unterprogramm zu verlassen, falls man sich vertan hat
            return lvs

        if name in lvs.keys():
            get = input("The Solution Vector already exists. Do you want to override it? [y/n]:")
            if get == "y":
                break
        else:
            break


    m = Matrix_classe.Matrix(2, 1) # just so my interpreter stops whining

    while True:
        try:
            zeilen = int(input("Anzahl der Zeilen: "))
        except ValueError:
            print("Kein Valider Input!")
        else:
            if zeilen > 1:
                break
            else:
                print("Muss mindestens 2 Zeilen haben!")

    while True:
        get = input("Soll der Lösungsvektor mit zufälligen Werten gefüllt werden? [y/n]:")

        if get == "y" or get == "yes":
            while True:
                try:
                    lowest_value = float(input("Gib den niedrigsten Wert ein welcher die Matrix beinhalten soll:"))
                except ValueError:
                    print("Keine Valide eingabe!")
                else:
                    break

            while True:
                try:
                    highest_value = float(input("Gib den höchsten Wert ein welcher die Matrix beinhalten soll:"))
                except ValueError:
                    print("Keine Valide eingabe!")
                else:
                    break

            m = extra_Funktionen_Matrix.random_matrix(1, zeilen, lowest_value, highest_value, debug_mode=debug_mode )
        elif get == "n" or get == "no":
            m = Matrix_classe.Matrix(zeilen, 1, debug=debug_mode)
            m.record_matrix()
        else:
            print("Keine Valide eingabe!")

        break

    lvs.update({name: m})
    print("Vektor erfolgreich erstellt!")
    return lvs

def debug_mode_toggle():
    """
    This function is called at the start to let the user toggle debug mode or not
    :return: True or False depending on user decision
    """
    system("cls")
    system("color 4")
    print("Do you want to activate DebugMode? [y/n]")
    get = input("/-> ")
    system("cls")
    system("color 2")
    if get == "y":
        print("DebugMode Activated!")
        return True
    else:
        print("DebugMode Deactivated!")
        return False

def terminal_start():
    """
    This function is the main function from which all the other functions in the code
    are controlled from
    :return: nothing, if this function ends, the programm ends
    """
    debug_mode = False

    if not debug_mode:
        system("color 8")
    print_help_menu(debug_mode)

    clean_mode = False
    matrizes = {}
    m = Matrix_classe.Matrix(3, 3, debug = debug_mode)
    m.set_matrix(np.array([[1,2,3], [1,2,3], [1,2,3]], dtype=float))
    m2 =  Matrix_classe.Matrix(3, 3, debug = debug_mode)
    m2.set_matrix(np.array([[2,4,3], [4,2,3], [3,4,3]], dtype=float))
    m3 = Matrix_classe.Matrix(4, 4, debug = debug_mode)
    m3.set_matrix(np.array([[0, 4, 3, 5], [4, 2, 10, 3], [3, 4, 3, 7], [3, 8, 3, 7]], dtype=float))
    matrizes.update({"bsp":m2})
    matrizes.update({"bsp_det0": m})
    matrizes.update({"x": m3})


    lvs = {}
    v = Matrix_classe.Matrix(3, 1)
    v.set_matrix(np.array([[1], [2], [3]], dtype=float))
    y = Matrix_classe.Matrix(4, 1)
    y.set_matrix(np.array([[1], [2], [3], [4]], dtype=float))
    lvs.update({"v":v})
    lvs.update({"y": y})

    if debug_mode:
        print(f"Beispielvektor:\n{lvs["v"]}")
        print(f"Beispielmatrix 1: \n{matrizes["bsp"]}")
        print(f"Beispielmatrix 2:\n{matrizes["bsp_det0"]}")

    while True:
        get = input("/> ")
        if get == "exit":
            system("color F") # reset terminal color to basic white
            break
        if get == "help":
            print_help_menu(debug_mode)
        if get == "cls":
            system("cls")
        if get == "cleanMode":
            if clean_mode:
                clean_mode = False
            else:
                clean_mode = True
                # damit der clean_mode direkt alles aufräumt
                system("cls"); print("/> cleanMode")
            print(f"Toggled cleanMode to {clean_mode}!")
        if get == "arithMode":
            matrizes = arith_mode(matrizes, clean_mode, debug_mode)
        if get == "det":
            matrizes = calc_determinant(matrizes, clean_mode, debug_mode)
        if get == "v":
            matrizes = calc_variables(matrizes, lvs, clean_mode, debug_mode)
        if get == "new m":
            matrizes = set_matrix(matrizes, clean_mode, debug_mode)
        if get == "new sv":
            lvs = set_solution_vector(lvs, clean_mode, debug_mode)
        if get == "current m":

            if clean_mode:
                system("cls")
                print("/> current m")

            keys = matrizes.keys()
            for k in keys:
                print(f"{k}:")
                print(matrizes[k])

        if get == "current sv":

            if clean_mode:
                system("cls")
                print("/> current sv")

            keys = lvs.keys()
            for k in keys:
                print(f"{k}:")
                print(lvs[k])

        if get == "debugMode":
            if debug_mode:
                if clean_mode:
                    system("cls")
                debug_mode = False
                system("color 8")
            else:
                if clean_mode:
                    system("cls")
                debug_mode = True
                system("color 2")

