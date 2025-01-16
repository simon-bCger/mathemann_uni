# jajajaja hier kommen noch tolle custom errors rein :)


class DeterminantZeroError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DimensionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UndefindProcessError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ExistenceError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)