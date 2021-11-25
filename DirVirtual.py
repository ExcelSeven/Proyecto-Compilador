import sys

class Dir:
    def __init__(self):
        self.gINT = 5000
        self.gFLOAT = 10000
        self.gCHAR = 15000
        self.lINT = 20000
        self.lFLOAT = 25000
        self.lCHAR = 30000
        self.tINT = 35000
        self.tFLOAT = 45000
        self.tBOOL = 55000
        self.tCHAR = 65000
        self.cINT = 70000
        self.cFLOAT = 80000
        self.cCHAR = 90000
        self.cSTRING = 100000
        self.pINT = 105000
        self.pFLOAT = 115000
        self.pCHAR = 125000

    def check(self):
        if self.gINT > 9999:
            print("Too many global integers.")
            sys.exit(0)
        elif self.gFLOAT > 14999:
            print("Too many global floating.")
            sys.exit(0)
        elif self.gCHAR > 19999:
            print("Too many global characters.")
            sys.exit(0)
        elif self.lINT > 24999:
            print("Too many local integers.")
            sys.exit(0)
        elif self.lFLOAT > 29999:
            print("Too many local floating.")
            sys.exit(0)
        elif self.lCHAR > 34999:
            print("Too many local characters.")
            sys.exit(0)
        elif self.tINT > 44999:
            print("Too many temporal integers.")
            sys.exit(0)
        elif self.tFLOAT > 54999:
            print("Too many temporal floating.")
            sys.exit(0)
        elif self.tBOOL > 64999:
            print("Too many temporal boolean.")
            sys.exit(0)
        elif self.tCHAR > 69999:
            print("Too many temporal boolean.")
            sys.exit(0)
        elif self.cINT > 79999:
            print("Too many constant integers.")
            sys.exit(0)
        elif self.cFLOAT > 89999:
            print("Too many constant floating.")
            sys.exit(0)
        elif self.cCHAR > 99999:
            print("Too many constant characters.")
            sys.exit(0)
        elif self.cSTRING > 104999:
            print("Too many constant characters.")
            sys.exit(0)
        elif self.pINT > 114999:
            print("Too many constant characters.")
            sys.exit(0)
        elif self.pFLOAT > 124999:
            print("Too many constant characters.")
            sys.exit(0)
        elif self.pCHAR > 134999:
            print("Too many constant characters.")
            sys.exit(0)
        else:
            pass