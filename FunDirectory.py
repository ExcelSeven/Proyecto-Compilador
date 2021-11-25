from VarTable import Var

class Fun:
    def __init__(self, type):
        self.return_type = type
        self.varTable = dict()
        self.signature = []
        self.direction = 1
        self.params = []
        self.size = [0, 0, 0, 0]      # int, float, char, bool