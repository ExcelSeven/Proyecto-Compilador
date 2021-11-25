from os import error
from re import I
from typing import IO
import DirVirtual
from DirVirtual import Dir
from Parser import quads, conTable
import Parser
import numpy as np
import matplotlib.pyplot as plt
import sys

class Exec:
    def __init__(self):
        self.value = 0
        self.vflag = 0
        self.vmem = 0

def assign(i):
    value = quads[iP.value][i]
    if value < 70000:
        if value in mMaster[mem[-1]].keys():
            if value < 10000 or (19999 < value < 25000) or (34999 < value < 45000):
                result = mMaster[mem[-1]][value]
            elif (9999 < value < 15000) or (24999 < value < 30000) or (44999 < value < 55000):
                result = mMaster[mem[-1]][value]
            else:
                result = mMaster[mem[-1]][value]
        else:
            print("Variable at direction %s does not have a value." % value)
            sys.exit(0)
    elif value < 105000:
        if value < 80000:
            result = int(conTable[value])
        elif quads[iP.value][1] < 90000:
            result = float(conTable[value])
        else:
            result = str(conTable[value])
    else:
        if mMaster[mem[-1]][value] in mMaster[mem[-1]].keys():
            if quads[iP.value][1] < 115000:
                result = mMaster[mem[-1]][mMaster[mem[-1]][value]]
            elif quads[iP.value][1] < 125000:
                result = mMaster[mem[-1]][mMaster[mem[-1]][value]]
            else:
                result = mMaster[mem[-1]][mMaster[mem[-1]][value]]
        else:
            print("Variable at direction %s does not have a value." % value)
            sys.exit(0)
    return(result)

def theMachine(action):
    if action == 1:
        leftOp = assign(1)
        rightOp = assign(2)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = leftOp + rightOp
        else:
            if iP.vflag == 1:
                mMaster[mem[-1]][quads[iP.value][3]] = leftOp + rightOp
                iP.vflag = 0
            else:
                mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = leftOp + rightOp
        iP.value += 1

    elif action == 2:
        leftOp = assign(1)
        rightOp = assign(2)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = leftOp - rightOp
        else:
            mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = leftOp - rightOp
        iP.value += 1

    elif action == 3:
        leftOp = assign(1)
        rightOp = assign(2)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = leftOp * rightOp
        else:
            mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = leftOp * rightOp
        iP.value += 1

    elif action == 4:
        leftOp = assign(1)
        rightOp = assign(2)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = leftOp / rightOp
        else:
            mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = leftOp / rightOp
        iP.value += 1

    elif action == 5:
        Op = assign(1)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = Op
        else:
            mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = Op
        iP.value += 1

    elif action == 6:
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp == rightOp
        iP.value += 1

    elif action == 7:
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp != rightOp
        iP.value += 1

    elif action == 8:
        leftOp = mMaster[mem[-1]][quads[iP.value][1]]
        rightOp = mMaster[mem[-1]][quads[iP.value][2]]
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp and rightOp
        iP.value += 1

    elif action == 9:
        leftOp = mMaster[mem[-1]][quads[iP.value][1]]
        rightOp = mMaster[mem[-1]][quads[iP.value][2]]
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp or rightOp
        iP.value += 1

    elif action == 10:
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp > rightOp
        iP.value += 1

    elif action == 11:     
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp < rightOp
        iP.value += 1

    elif action == 12:
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp >= rightOp
        iP.value += 1

    elif action == 13:
        leftOp = assign(1)
        rightOp = assign(2)
        mMaster[mem[-1]][quads[iP.value][3]] = leftOp <= rightOp
        iP.value += 1

    elif action == 14:
        Op = assign(1)
        mMaster[mem[-2]][quads[iP.value][3]] = Op
        iP.value += 1

    elif action == 15:
        if quads[iP.value][3] < 10000 or (19999 < quads[iP.value][3] < 25000) or (34999 < quads[iP.value][3] < 45000) or (104999 < quads[iP.value][3] < 115000):
            try:
                Op = int(input("Input an integer: "))
            except:
                print("Value inputted not integer.")
                sys.exit(0)
        elif (9999 < quads[iP.value][3] < 15000) or (24999 < quads[iP.value][3] < 30000) or (44999 < quads[iP.value][3] < 55000) or (114999 < quads[iP.value][3] < 125000):
            try:
                Op = float(input("Input a floating number: "))
            except:
                print("Value inputted not floating.")
                sys.exit(0)
        else:
            try:
                Op = str(input("Input character: "))
            except:
                print("Value inputted not character.")
                sys.exit(0)
        if quads[iP.value][3] < 105000:
            mMaster[mem[-1]][quads[iP.value][3]] = Op
        else:
            mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]] = Op  
        iP.value += 1

    elif action == 16:
        if quads[iP.value][3] < 70000:
            print(mMaster[mem[-1]][quads[iP.value][3]])
        elif quads[iP.value][3] < 105000:
            if type(conTable[quads[iP.value][3]]) == str:
                res = conTable[quads[iP.value][3]]
                print(res[1:-1])
            else:
                print(conTable[quads[iP.value][3]])
        else:
            print(mMaster[mem[-1]][mMaster[mem[-1]][quads[iP.value][3]]])
        iP.value += 1

    elif action == 17:
        iP.value = (quads[iP.value][3] - 1)

    elif action == 18:
        if mMaster[mem[-1]][quads[iP.value][1]] == False:
            iP.value = (quads[iP.value][3] - 1)
        else:
            iP.value += 1

    elif action == 19:
        del mMaster[mem[-1]]
        mem.pop()
        iP.value = (exJumps.pop() + 1)

    elif action == 20:
        iP.vmem += 1
        mem.append(iP.vmem)
        if len(mem) > 300:
            print("Too much memory space used.")
            sys.exit(0)
        mMaster[mem[-1]] = dict()
        mMaster[mem[-1]].update(mMaster[mem[-2]])
        iP.value += 1

    elif action == 21:
        Op = assign(1)
        mMaster[mem[-1]][quads[iP.value][3]] = Op
        iP.value += 1

    elif action == 22:
        exJumps.append(iP.value)
        iP.value = (quads[iP.value][3] - 1)

    elif action == 23:
        if quads[iP.value][1] < 70000:
            if quads[iP.value][1] in mMaster[mem[-1]].keys():
                leftOp = int(mMaster[mem[-1]][quads[iP.value][1]])
            else:
                print("Variable at direction %s does not have a value." % quads[iP.value][1])
                sys.exit(0)
        else:
            leftOp = int(conTable[quads[iP.value][1]])
        rightOp = int(conTable[quads[iP.value][2]])
        if -1 < leftOp < rightOp:
            pass
        else:
            print("Index out of range for variable in direction %s." % quads[iP.value][3])
            sys.exit(0)
        iP.value += 1
        iP.vflag = 1

    elif action == 24:
        Op = sum(vectA) / len(vectA)
        mMaster[mem[-1]][quads[iP.value][3]] = Op
        vectA.clear()
        iP.value += 1

    elif action == 25:
        Op = max(set(vectA), key=vectA.count)
        mMaster[mem[-1]][quads[iP.value][3]] = Op
        vectA.clear()
        iP.value += 1

    elif action == 26:
        avg = sum(vectA) / len(vectA)
        Op = sum((x-avg)**2 for x in vectA) / len(vectA)
        mMaster[mem[-1]][quads[iP.value][3]] = Op
        vectA.clear()
        iP.value += 1

    elif action == 27:
        x = np.array(vectA)
        y = np.array(vectB)
        plt.plot(x, y, 'o')
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b)      
        plt.show()
        vectA.clear()
        vectB.clear()
        iP.value += 1 

    elif action == 28:
        x = np.array(vectA)
        y = np.array(vectB)
        plt.plot(x, y)      
        plt.show()
        vectA.clear()
        vectB.clear()
        iP.value += 1 

    elif action == 29:
        Op = assign(1)
        for i in range (0, Op):
            if quads[iP.value][3] + i in mMaster[mem[-1]].keys():
                vectA.append(mMaster[mem[-1]][quads[iP.value][3] + i])
            else:
                print("Array given to special function has empty values.")
                sys.exit(0)
        iP.value += 1

    elif action == 30:
        Op = assign(1)
        for i in range (0, Op):
            if quads[iP.value][3] + i in mMaster[mem[-1]].keys():
                vectB.append(mMaster[mem[-1]][quads[iP.value][3] + i])
            else:
                print("Array given to special function has empty values.")
                sys.exit(0)
        iP.value += 1


iP = Exec()

mem = []
mem.append(0)

mMaster = dict()

mMaster[mem[-1]] = dict()

exJumps = []

vectA = []
vectB = []

while iP.value + 1 <= len(Parser.quads):
    theMachine(Parser.quads[iP.value][0])