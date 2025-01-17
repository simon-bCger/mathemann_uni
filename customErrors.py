# jajajaja hier kommen noch tolle custom errors rein :)
# hu hier sind tolle errors rein gekommen


class DeterminantZeroError(Exception):
    """
    This error should be used when the Determinant of a Matrix is zero
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DimensionError(Exception):
    """
    This error is used to signal if one try's to calculate the Determinant of a Matrix with unequal Dimensions
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UndefindProcessError(Exception):
    """
    This error is used if somehow the user was able to select a nonexistent Process
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ExistenceError(Exception):
    """
    This error is thrown if something in the Matrix does not exist or already exists
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SlipUpError(Exception):
    """
    This error is thrown if something happens that shouldn't, like a user choosing a none existent arithmetic operator
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)