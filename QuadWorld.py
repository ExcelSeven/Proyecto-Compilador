class Time:
    def __init__(self):
        self.currentType = "program"
        self.currentScope = "global"
        self.currentFunction = ""
        self.currentProgram = ""
        self.currentTemp = 1
        self.currentPoint = 1
        self.currentQuad = 1
        self.currentVoid = 0
        self.paramStatus = 0
        self.paramCount = 1
        self.paramFun = ""
