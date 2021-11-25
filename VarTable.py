class Var:
    def __init__(self, type, scope):
        self.type = type
        self.scope = scope
        self.size = 0
        self.dir = 0