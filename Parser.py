import os
from types import FunctionType
import types
import ply.yacc as yacc     
import Lexer                
from VarTable import Var
from QuadWorld import Time
from FunDirectory import Fun
from SemCube import resultingType
from DirVirtual import Dir
import sys

def get_key(val):
    for key, value in conTable.items():
         if val == value:
             return key

tokens = Lexer.tokens

Passage = Time()

oStack = []
opStack = []
typeStack = []
jumpStack = []

masterStack = []

quads = []

def p_program_structure(p):
    '''program_structure : PROGRAM initiate ID addfun addprog SEMI declare_var changescope functions MAIN changeback LPAREN RPAREN LCURLY statutes RCURLY endfunc
                         | PROGRAM initiate ID addfun addprog SEMI declare_var changescope MAIN changeback LPAREN RPAREN LCURLY statutes RCURLY endfunc
                         | PROGRAM initiate ID addfun addprog SEMI changescope functions MAIN changeback LPAREN RPAREN LCURLY statutes RCURLY endfunc
                         | PROGRAM initiate ID addfun addprog SEMI MAIN changeback LPAREN RPAREN LCURLY statutes RCURLY endfunc'''

def p_addprog(p):
    '''addprog :'''
    Passage.currentProgram = p[-2]

def p_initiate(p):
    '''initiate :'''
    global functionDirectory
    functionDirectory = dict()
    global conTable
    conTable = dict()
    global virtualMemory
    virtualMemory = Dir()
    quads.append([17, -1, -1, -1])
    jumpStack.append(Passage.currentQuad)
    virtualMemory.check()
    conTable[virtualMemory.cINT] = "1"
    virtualMemory.cINT += 1
    Passage.currentQuad += 1

def p_addfun(p):
    '''addfun :'''
    if p[-1] in functionDirectory:
        print("Function ID %s is a duplicate name." % p[-1])
        sys.exit(0)
    else:
        functionDirectory[p[-1]] = Fun(Passage.currentType)
        if Passage.currentScope == "local":
            if Passage.currentType != "void":
                functionDirectory[Passage.currentProgram].varTable[p[-1]] = Var(Passage.currentType, "global")
                if Passage.currentType == "int":
                    virtualMemory.check()
                    functionDirectory[Passage.currentProgram].varTable[p[-1]].dir = virtualMemory.gINT
                    virtualMemory.gINT += 1        
                    functionDirectory[p[-1]].size[0] += 1
                elif Passage.currentType == "float":
                    virtualMemory.check()
                    functionDirectory[Passage.currentProgram].varTable[p[-1]].dir = virtualMemory.gFLOAT
                    virtualMemory.gFLOAT += 1    
                    functionDirectory[p[-1]].size[1] += 1
                elif Passage.currentType == "char":
                    virtualMemory.check()
                    functionDirectory[Passage.currentProgram].varTable[p[-1]].dir = virtualMemory.gCHAR
                    virtualMemory.gCHAR += 1    
                    functionDirectory[p[-1]].size[2] += 1
            functionDirectory[p[-1]].varTable.update(functionDirectory[Passage.currentProgram].varTable) 
            functionDirectory[p[-1]].size[0] += functionDirectory[Passage.currentProgram].size[0]
            functionDirectory[p[-1]].size[1] += functionDirectory[Passage.currentProgram].size[1]
            functionDirectory[p[-1]].size[2] += functionDirectory[Passage.currentProgram].size[2]
            functionDirectory[p[-1]].size[3] += functionDirectory[Passage.currentProgram].size[3]
        Passage.currentFunction = p[-1]
        Passage.currentTemp = 1
        virtualMemory.lINT = 20000
        virtualMemory.lFLOAT = 25000
        virtualMemory.lCHAR = 30000
        virtualMemory.tINT = 35000
        virtualMemory.tFLOAT = 45000
        virtualMemory.tBOOL = 55000
        virtualMemory.tCHAR = 65000
        functionDirectory[p[-1]].direction = Passage.currentQuad

def p_changescope(p):
    '''changescope :'''
    Passage.currentScope = "local"

def p_changeback(p):
    '''changeback :'''
    Passage.currentFunction = Passage.currentProgram
    Passage.currentTemp = 1
    virtualMemory.tINT = 35000
    virtualMemory.tFLOAT = 45000
    virtualMemory.tBOOL = 55000
    virtualMemory.tCHAR = 65000
    Passage.currentVoid = 1
    main = jumpStack.pop()
    quads[main-1][3] = Passage.currentQuad

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR''' 
    p[0] = p[1]

def p_declare_var(p):
    '''declare_var : VARS multitypes'''

def p_multitypes(p):
    '''multitypes : type addtype COLON multivars SEMI
                  | type addtype COLON multivars SEMI multitypes'''
    
def p_addtype(p):
    '''addtype :'''
    Passage.currentType = p[-1]
    if p[-1] == "void":
        Passage.currentVoid = 1

def p_multivars(p):
    '''multivars : ID addvar
                 | ID addvar COMMA multivars
                 | dimvars addvard
                 | dimvars addvard COMMA multivars'''

def p_dimvars(p):
    '''dimvars : ID LBRACK expr RBRACK'''
    p[0] = p[1]

def p_addvar(p):
    '''addvar :'''
    if p[-1] in functionDirectory[Passage.currentFunction].varTable:
        print("Variable ID %s is a duplicate name." % p[-1])
        sys.exit(0)
    else: 
        functionDirectory[Passage.currentFunction].varTable[p[-1]] = Var(Passage.currentType, Passage.currentScope)
        if Passage.paramStatus == 1:
            functionDirectory[Passage.currentFunction].signature.append(Passage.currentType)
        if Passage.currentScope == "global":
            if Passage.currentType == "int":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gINT
                virtualMemory.gINT += 1          
                functionDirectory[Passage.currentFunction].size[0] += 1  
            elif Passage.currentType == "float":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gFLOAT
                virtualMemory.gFLOAT += 1            
                functionDirectory[Passage.currentFunction].size[1] += 1  
            else:
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gCHAR
                virtualMemory.gCHAR += 1                
                functionDirectory[Passage.currentFunction].size[2] += 1
        else:
            if Passage.currentType == "int":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lINT
                virtualMemory.lINT += 1        
                functionDirectory[Passage.currentFunction].size[0] += 1    
            elif Passage.currentType == "float":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lFLOAT
                virtualMemory.lFLOAT += 1     
                functionDirectory[Passage.currentFunction].size[1] += 1         
            else:
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lCHAR
                virtualMemory.lCHAR += 1 
                functionDirectory[Passage.currentFunction].size[2] += 1
        functionDirectory[Passage.currentFunction].params.append(functionDirectory[Passage.currentFunction].varTable[p[-1]].dir)

def p_addvard(p):
    '''addvard :'''
    if p[-1] in functionDirectory[Passage.currentFunction].varTable:
        print("Variable ID %s is a duplicate name." % p[-4])
        sys.exit(0)
    else: 
        rOp = oStack.pop()
        rType = typeStack.pop()
        if rType != "int":
            print("Declared dimensioned variable %s with a non integer size" % p[-1])
            sys.exit(0)
        else:
            functionDirectory[Passage.currentFunction].varTable[p[-1]] = Var(Passage.currentType, Passage.currentScope)
            functionDirectory[Passage.currentFunction].varTable[p[-1]].size = rOp         
            if Passage.paramStatus == 1:
                print("Call-based dimensioned variables cannot be declared in functions.")
                sys.exit(0)   
        if Passage.currentScope == "global":
                if Passage.currentType == "int":
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gINT
                    virtualMemory.gINT += int(rOp)       
                    functionDirectory[Passage.currentFunction].size[0] += int(rOp)  
                elif Passage.currentType == "float":
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gFLOAT
                    virtualMemory.gFLOAT += int(rOp)              
                    functionDirectory[Passage.currentFunction].size[1] += int(rOp)    
                else:
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.gCHAR
                    virtualMemory.gCHAR += int(rOp)                  
                    functionDirectory[Passage.currentFunction].size[2] += int(rOp)  
        else:
            if Passage.currentType == "int":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lINT
                virtualMemory.lINT += int(rOp)          
                functionDirectory[Passage.currentFunction].size[0] += int(rOp)      
            elif Passage.currentType == "float":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lFLOAT
                virtualMemory.lFLOAT += int(rOp)       
                functionDirectory[Passage.currentFunction].size[1] += int(rOp)           
            else:
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable[p[-1]].dir = virtualMemory.lCHAR
                virtualMemory.lCHAR += int(rOp)   
                functionDirectory[Passage.currentFunction].size[2] += int(rOp)  

def p_return_type(p):
    '''return_type : INT
                   | FLOAT
                   | CHAR
                   | VOID'''
    p[0] = p[1]

def p_declare_fun(p):
    '''declare_fun : FUNCTION return_type addtype ID addfun LPAREN RPAREN
                   | FUNCTION return_type addtype ID addfun LPAREN paramstatus params paramstatus RPAREN'''

def p_functions(p):
    '''functions : declare_fun declare_var LCURLY statutes RCURLY endfunc
                 | declare_fun LCURLY statutes RCURLY endfunc
                 | declare_fun declare_var LCURLY statutes RCURLY endfunc functions
                 | declare_fun LCURLY statutes RCURLY endfunc functions'''

def p_endfunc(p):
    '''endfunc :'''
    if Passage.currentVoid != 1 and quads[Passage.currentQuad - 2][0] != 14:
        print("No return used in non-void function %s." % (Passage.currentFunction))
        sys.exit(0)
    else:
        functionDirectory[Passage.currentFunction].varTable = dict()
        if Passage.currentFunction != Passage.currentProgram:
            quads.append([19, -1, -1, -1])
            Passage.currentVoid = 0
            Passage.currentQuad += 1

def p_paramstatus(p):
    '''paramstatus :'''
    if Passage.paramStatus == 0:
        Passage.paramStatus = 1
    else:
        Passage.paramStatus = 0

def p_params(p):
    '''params : type addtype COLON multivars
              | type addtype COLON multivars SEMI params'''

def p_statutes(p):
    '''statutes : assign
                | assign statutes
                | call_void
                | call_void statutes
                | returning
                | reading
                | reading statutes
                | writing
                | writing statutes
                | decision
                | decision statutes
                | conditional
                | conditional statutes
                | nonconditional
                | nonconditional statutes'''

def p_assign(p):
    '''assign : ID pushid EQUALS exprs assignment SEMI
              | ID pushid LBRACK exprs RBRACK verif EQUALS exprs assignment SEMI'''

def p_assignment(p):
    '''assignment :'''
    rightOp = oStack.pop()
    leftOp = oStack.pop()
    rightType = typeStack.pop()
    leftType = typeStack.pop()
    resType = resultingType("=", leftType, rightType)
    if resType != "ERROR":
        if rightOp in conTable.values():
            quads.append([5, get_key(rightOp), -1, functionDirectory[Passage.currentFunction].varTable[leftOp].dir])
            Passage.currentQuad += 1
        else:
            quads.append([5, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, -1, functionDirectory[Passage.currentFunction].varTable[leftOp].dir])
            Passage.currentQuad += 1
    else:
        print("Type mismatch between %s and %d." % (leftOp, rightOp))
        sys.exit(0)

def p_call_void(p):
    '''call_void : ID call exprp confirm SEMI
                 | ID call LPAREN RPAREN confirm SEMI
                 | special2 exprp sconfirm2 SEMI'''

def p_special2(p):
    '''special2 : REGRESION
                | PLOT'''
    p[0] = p[1]

def p_sconfirm2(p):
    '''sconfirm2 :'''
    rightOp = oStack.pop()
    rightType = typeStack.pop()
    leftOp = oStack.pop()
    leftType = typeStack.pop()
    if functionDirectory[Passage.currentFunction].varTable[rightOp].size == 0 or functionDirectory[Passage.currentFunction].varTable[leftOp].size == 0:
        print("Called special function %s without an array." % p[-2])
        sys.exit(0)
    else:
        if rightType == "char" or leftType == "char":
            print("Called special function %s with a non-numerical array." % p[-2])
        else:
            if functionDirectory[Passage.currentFunction].varTable[leftOp].size == functionDirectory[Passage.currentFunction].varTable[rightOp].size:
                quads.append([29, get_key(functionDirectory[Passage.currentFunction].varTable[leftOp].size), -1, functionDirectory[Passage.currentFunction].varTable[leftOp].dir])
                Passage.currentQuad += 1
                quads.append([30, get_key(functionDirectory[Passage.currentFunction].varTable[rightOp].size), -1, functionDirectory[Passage.currentFunction].varTable[rightOp].dir])
                Passage.currentQuad += 1
                if p[-2] == "regresion":
                    quads.append([27, -1, -1, -1])
                elif p[-2] == "plot":
                    quads.append([28, -1, -1, -1])    
                Passage.currentQuad += 1
            else:
                print("Using arrays of different sizes in special function.")
                sys.exit(0)

def p_returning(p):
    '''returning : RETURN LPAREN exprs returnquad RPAREN SEMI'''

def p_returnquad(p):
    '''returnquad :'''
    if Passage.currentVoid != 1:
        rOp = oStack.pop()
        rType = typeStack.pop()
        if rType != functionDirectory[Passage.currentFunction].return_type:
            print("Type of expression returned different from %s return type." % Passage.currentFunction)
            sys.exit(0)
        else:
            if rOp in conTable.values():
                quads.append([14, get_key(rOp), -1, functionDirectory[Passage.currentProgram].varTable[Passage.currentFunction].dir])
            else:
                quads.append([14, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.currentProgram].varTable[Passage.currentFunction].dir])
            Passage.currentQuad += 1
    else:
        print("Illegal use of return on void function %s." % (Passage.currentFunction))
        sys.exit(0)

def p_reading(p):
    '''reading : READ LPAREN read_opt RPAREN SEMI'''

def p_read_opt(p):
    '''read_opt : expr readquad
                | expr readquad COMMA read_opt'''

def p_readquad(p):
    '''readquad :'''
    rOp = oStack.pop()
    rType = typeStack.pop()
    quads.append([15, -1, -1, functionDirectory[Passage.currentFunction].varTable[rOp].dir])
    Passage.currentQuad += 1

def p_writing(p):
    '''writing : WRITE LPAREN write_opt RPAREN SEMI'''

def p_write_opt(p):
    '''write_opt : MESSAGE writequad1
                 | MESSAGE writequad1 COMMA write_opt
                 | exprs writequad2
                 | exprs writequad2 COMMA write_opt'''

def p_writequad1(p):
    '''writequad1 :'''
    rOp = p[-1]
    virtualMemory.check()
    conTable[virtualMemory.cSTRING] = p[-1]
    virtualMemory.cSTRING += 1
    quads.append([16, -1, -1, get_key(p[-1])])
    Passage.currentQuad += 1

def p_writequad2(p):
    '''writequad2 :'''
    rOp = oStack.pop()
    rType = typeStack.pop()
    if rOp in conTable.values():
        quads.append([16, -1, -1, get_key(rOp)])
    else:
        quads.append([16, -1, -1, functionDirectory[Passage.currentFunction].varTable[rOp].dir])
    Passage.currentQuad += 1

def p_decision(p):
    '''decision : IF LPAREN logic RPAREN ifquad THEN LCURLY statutes RCURLY filljump
                | IF LPAREN logic RPAREN ifquad THEN LCURLY statutes RCURLY ELSE elsequad LCURLY statutes RCURLY filljump'''

def p_ifquad(p):
    '''ifquad :'''
    rType = typeStack.pop()
    if rType == "bool":
        rOp = oStack.pop()
        quads.append([18, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, -1])
        jumpStack.append(Passage.currentQuad)
        Passage.currentQuad += 1
    else:
        print("Type mismatch, condition is not boolean.")
        sys.exit(0)

def p_elsequad(p):
    '''elsequad :'''
    quads.append([17, -1, -1, -1])
    false = jumpStack.pop()
    jumpStack.append(Passage.currentQuad)
    quads[false-1][3] = Passage.currentQuad + 1
    Passage.currentQuad += 1

def p_filljump(p):
    '''filljump :'''
    end = jumpStack.pop()
    quads[end-1][3] = Passage.currentQuad

def p_conditional(p):
    '''conditional : WHILE loopquad LPAREN logic RPAREN whilequad DO LCURLY statutes RCURLY endquad'''

def p_loopquad(p):
    '''loopquad :'''
    jumpStack.append(Passage.currentQuad)

def p_whilequad(p):
    '''whilequad :'''
    rType = typeStack.pop()
    if rType == "bool":
        rOp = oStack.pop()
        quads.append([18, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, -1])
        jumpStack.append(Passage.currentQuad)
        Passage.currentQuad += 1
    else:
        print("Type mismatch, condition is not boolean.")
        sys.exit(0)

def p_endquad(p):
    '''endquad :'''
    end = jumpStack.pop()
    again = jumpStack.pop()
    quads.append([17, -1, -1, again])
    quads[end-1][3] = Passage.currentQuad + 1
    Passage.currentQuad += 1

def p_logic(p):
    '''logic : relation AND relation logicquad
             | relation OR relation logicquad
             | relation'''

def p_relation(p):
    '''relation : exprs GREATER exprs logicquad
                | exprs GREATER_EQ exprs logicquad
                | exprs LESSER exprs logicquad
                | exprs LESSER_EQ exprs logicquad
                | exprs COMPARE exprs logicquad
                | exprs DIFFERENT exprs logicquad'''

def p_logicquad(p):
    '''logicquad :'''
    rightOp = oStack.pop()
    leftOp = oStack.pop()
    rightType = typeStack.pop()
    leftType = typeStack.pop()
    operator = p[-2]
    resType = resultingType(operator, leftType, rightType)
    if resType != "ERROR":
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("bool", "temporal")
        virtualMemory.check()
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tBOOL
        virtualMemory.tBOOL += 1
        functionDirectory[Passage.currentFunction].size[3] += 1
        oStack.append("t%s" % Passage.currentTemp)
        typeStack.append(resType)
        if operator == ">":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([10, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([10, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([10, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([10, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])   
        elif operator == ">=":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([12, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([12, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([12, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([12, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])          
        elif operator == "<":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([11, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([11, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([11, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([11, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])   
        elif operator == "<=":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([13, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([13, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([13, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([13, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])       
        elif operator == "==":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([6, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([6, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([6, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([6, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])        
        elif operator == "!=":
            if leftOp in conTable.values() and rightOp in conTable.values():
                quads.append([7, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif leftOp in conTable.values():
                quads.append([7, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif rightOp in conTable.values():
                quads.append([7, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([7, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])        
        elif operator == "&":
            quads.append([8, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
        elif operator == "|":
            quads.append([9, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
        Passage.currentTemp += 1      
        Passage.currentQuad += 1  
    else:
        print("Type mismatch in logic operation between %s and %d." % (leftOp, rightOp))
        sys.exit(0)

def p_nonconditional(p):
    '''nonconditional : FOR exprs forquad1 EQUALS exprs forquad2 TO exprs forquad3 DO LCURLY statutes RCURLY forquad4'''

def p_forquad1(p):
    '''forquad1 :'''
    if typeStack[-1] == "int" or typeStack[-1] == "float":
        pass
    else:
        print("Type mismatch. Variable %s is not numeric." % (oStack[-1]))
        sys.exit(0)

def p_forquad2(p):
    '''forquad2 :'''
    rType = typeStack.pop()
    rOp = oStack.pop()
    if rType == "int" or rType == "float":
        vMaster = oStack[-1]
        tMaster = typeStack[-1]
        masterStack.append(Passage.currentTemp)
        resType = resultingType("=", tMaster, rType)
        if resType != "ERROR":
            if rOp in conTable.values():
                quads.append([5, get_key(rOp), -1, functionDirectory[Passage.currentFunction].varTable[vMaster].dir])
            else:
                quads.append([5, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.currentFunction].varTable[vMaster].dir])
            Passage.currentQuad += 1
            if resType == "int":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("int", "temporal")
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
                virtualMemory.tINT += 1
                functionDirectory[Passage.currentFunction].size[0] += 1
            else:
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("float", "temporal")
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
                virtualMemory.tFLOAT += 1
                functionDirectory[Passage.currentFunction].size[1] += 1
            if rOp in conTable.values():
                quads.append([5, get_key(rOp), -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            else:
                quads.append([5, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            Passage.currentQuad += 1  
            Passage.currentTemp += 1
        else:
            print("Type mismatch between %s and %d." % (vMaster, rOp))
            sys.exit(0)
    else:
        print("Type mismatch. Variable %s is not numeric." % (rOp))
        sys.exit(0)

def p_forquad3(p):
    '''forquad3 :'''
    rType = typeStack.pop()
    rOp = oStack.pop()
    if rType == "int" or rType == "float":
        if rType == "int":
            functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("int", "temporal")
            virtualMemory.check()
            functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
            virtualMemory.tINT += 1
            functionDirectory[Passage.currentFunction].size[0] += 1
        else:
            functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("float", "temporal")
            virtualMemory.check()
            functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
            virtualMemory.tFLOAT += 1
            functionDirectory[Passage.currentFunction].size[1] += 1
        if rOp in conTable.values():
            quads.append([5, get_key(rOp), -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
        else:
            quads.append([5, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])        
        Passage.currentQuad += 1
        Passage.currentTemp += 1
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("bool", "temporal")
        virtualMemory.check()
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tBOOL
        virtualMemory.tBOOL += 1
        functionDirectory[Passage.currentFunction].size[3] += 1
        quads.append([11, functionDirectory[Passage.currentFunction].varTable["t%s" % (masterStack[-1])].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % (Passage.currentTemp - 1)].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])        
        jumpStack.append(Passage.currentQuad)
        Passage.currentQuad += 1
        quads.append([18, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir, -1, -1])
        jumpStack.append(Passage.currentQuad)
        Passage.currentQuad += 1
        Passage.currentTemp += 1
    else:
        print("Type mismatch. Variable %s is not numeric." % (rOp))
        sys.exit(0)

def p_forquad4(p):
    '''forquad4 :'''
    if functionDirectory[Passage.currentFunction].varTable["t%s" % (masterStack[-1])].type == "int":
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("int", "temporal")
        virtualMemory.check()
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
        virtualMemory.tINT += 1
        functionDirectory[Passage.currentFunction].size[0] += 1
    else:
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("float", "temporal")
        virtualMemory.check()
        functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
        virtualMemory.tFLOAT += 1
        functionDirectory[Passage.currentFunction].size[1] += 1
    quads.append([1, functionDirectory[Passage.currentFunction].varTable["t%s" % (masterStack[-1])].dir, get_key("1"), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
    Passage.currentQuad += 1
    quads.append([5, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % (masterStack[-1])].dir])
    Passage.currentQuad += 1
    quads.append([5, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir, -1, functionDirectory[Passage.currentFunction].varTable[oStack[-1]].dir])
    Passage.currentQuad += 1
    end = jumpStack.pop()
    again = jumpStack.pop()
    quads.append([17, -1, -1, again])
    quads[end-1][3] = Passage.currentQuad + 1
    oStack.pop()
    typeStack.pop()
    masterStack.pop()
    Passage.currentQuad += 1
    Passage.currentTemp += 1

def p_exprs(p):
    '''exprs : expr pams
             | expr pams COMMA exprs
             | exprp pams 
             | exprp pams COMMA exprs'''

def p_exprp(p):
    '''exprp : LPAREN pushop exprs RPAREN popop '''

def p_popop(p):
    '''popop :'''
    opStack.pop()

def p_expr(p):
    '''expr : expr PLUS pushop term quad1 
            | expr MINUS pushop term quad1
            | term quad1'''

def p_term(p):
    '''term : term TIMES pushop factor quad2
            | term DIVIDE pushop factor quad2
            | factor quad2'''

def p_quad1(p):
    '''quad1 :'''
    if len(opStack) > 0:
        if opStack[-1] == '+' or opStack[-1] == '-':
            rightOp = oStack.pop()
            leftOp = oStack.pop()
            rightType = typeStack.pop()
            leftType = typeStack.pop()
            operator = opStack.pop()
            resType = resultingType(operator, leftType, rightType)
            if resType != "ERROR":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var(resType, "temporal")
                if resType == "int":
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
                    virtualMemory.tINT += 1
                    functionDirectory[Passage.currentFunction].size[0] += 1
                else:
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
                    virtualMemory.tFLOAT += 1
                    functionDirectory[Passage.currentFunction].size[1] += 1
                oStack.append("t%s" % Passage.currentTemp)
                typeStack.append(resType)
                if operator == "+":
                    if leftOp in conTable.values() and rightOp in conTable.values():
                        quads.append([1, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif leftOp in conTable.values():
                        quads.append([1, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif rightOp in conTable.values():
                        quads.append([1, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    else:
                        quads.append([1, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])   
                elif operator == "-":
                    if leftOp in conTable.values() and rightOp in conTable.values():
                        quads.append([2, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif leftOp in conTable.values():
                        quads.append([2, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif rightOp in conTable.values():
                        quads.append([2, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    else:
                        quads.append([2, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])   
                Passage.currentTemp += 1
                Passage.currentQuad += 1
            else:
                print("Type mismatch between %s and %d." % (leftOp, rightOp))
                sys.exit(0)
        else:
            pass
    else:
        pass

def p_quad2(p):
    '''quad2 :'''
    if len(opStack) > 0:
        if opStack[-1] == '*' or opStack[-1] == '/':
            rightOp = oStack.pop()
            leftOp = oStack.pop()
            rightType = typeStack.pop()
            leftType = typeStack.pop()
            operator = opStack.pop()
            resType = resultingType(operator, leftType, rightType)
            if resType != "ERROR":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var(resType, "temporal")
                if resType == "int":
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
                    virtualMemory.tINT += 1
                    functionDirectory[Passage.currentFunction].size[0] += 1
                else:
                    virtualMemory.check()
                    functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
                    virtualMemory.tFLOAT += 1
                    functionDirectory[Passage.currentFunction].size[1] += 1
                oStack.append("t%s" % Passage.currentTemp)
                typeStack.append(resType)
                if operator == "*":
                    if leftOp in conTable.values() and rightOp in conTable.values():
                        quads.append([3, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif leftOp in conTable.values():
                        quads.append([3, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif rightOp in conTable.values():
                        quads.append([3, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    else:
                        quads.append([3, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])   
                elif operator == "/":
                    if leftOp in conTable.values() and rightOp in conTable.values():
                        quads.append([4, get_key(leftOp), get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif leftOp in conTable.values():
                        quads.append([4, get_key(leftOp), functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    elif rightOp in conTable.values():
                        quads.append([4, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, get_key(rightOp), functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
                    else:
                        quads.append([4, functionDirectory[Passage.currentFunction].varTable[leftOp].dir, functionDirectory[Passage.currentFunction].varTable[rightOp].dir, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])                   
                Passage.currentTemp += 1
                Passage.currentQuad += 1
            else:
                print("Type mismatch between %s and %d." % (leftOp, rightOp))
                sys.exit(0)
        else:
            pass
    else:
        pass

def p_pushop(p):
    '''pushop :'''
    opStack.append(p[-1])

def p_factor(p):
    '''factor : C_INT pushint
              | MINUS C_INT pushintn
              | C_FLOAT pushfloat
              | MINUS C_FLOAT pushfloatn
              | C_CHAR pushchar 
              | ID pushid
              | ID pushid LBRACK exprs RBRACK verif
              | ID call LPAREN RPAREN confirm
              | ID call exprp confirm
              | special1 exprp sconfirm1'''

def p_special1(p):
    '''special1 : MEDIA
                | MODA
                | VARIANZA'''
    p[0] = p[1]

def p_sconfirm1(p):
    '''sconfirm1 :'''
    rOp = oStack.pop()
    rType = typeStack.pop()
    if functionDirectory[Passage.currentFunction].varTable[rOp].size == 0:
        print("Called special function %s without an array." % p[-2])
        sys.exit(0)
    else:
        if rType == "char":
            print("Called special function %s with a non-numerical array." % p[-2])
        else: 
            quads.append([29, get_key(functionDirectory[Passage.currentFunction].varTable[rOp].size), -1, functionDirectory[Passage.currentFunction].varTable[rOp].dir])
            Passage.currentQuad += 1
            functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var(rType, "temporal")
            if rType == "int":
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
                virtualMemory.tINT += 1            
            else:
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
                virtualMemory.tFLOAT += 1  
            if p[-2] == "media":
                quads.append([24, -1, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif p[-2] == "moda":
                quads.append([25, -1, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            elif p[-2] == "varianza":
                quads.append([26, -1, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
        Passage.currentQuad += 1
        oStack.append("t%s" % Passage.currentTemp)
        typeStack.append(rType)

def p_pushid(p):
    '''pushid :'''
    if p[-1] in functionDirectory[Passage.currentFunction].varTable:
        oStack.append(p[-1])
        typeStack.append(functionDirectory[Passage.currentFunction].varTable[p[-1]].type)
    else:
        print("Unidentified variable %s." % (p[-1]))
        sys.exit(0)

def p_pushint(p):
    '''pushint :'''
    oStack.append(p[-1])
    typeStack.append("int")
    if p[-1] not in conTable.values():
        virtualMemory.check()
        conTable[virtualMemory.cINT] = p[-1]
        virtualMemory.cINT += 1
    else:
        pass

def p_pushintn(p):
    '''pushintn :'''
    oStack.append("-%s" % (p[-1]))
    typeStack.append("int")
    if "-%s" % (p[-1]) not in conTable.values():
        virtualMemory.check()
        conTable[virtualMemory.cINT] = "-%s" % (p[-1])
        virtualMemory.cINT += 1
    else:
        pass

def p_pushfloat(p):
    '''pushfloat :'''
    oStack.append(p[-1])
    typeStack.append("float")
    if p[-1] not in conTable.values():
        virtualMemory.check()
        conTable[virtualMemory.cFLOAT] = p[-1]
        virtualMemory.cFLOAT += 1
    else:
        pass

def p_pushfloatn(p):
    '''pushfloatn :'''
    oStack.append("-%s" % (p[-1]))
    typeStack.append("float")
    if "-%s" % (p[-1]) not in conTable.values():
        virtualMemory.check()
        conTable[virtualMemory.cFLOAT] = "-%s" % (p[-1])
        virtualMemory.cFLOAT += 1
    else:
        pass

def p_pushchar(p):
    '''pushchar :'''
    oStack.append(p[-1])
    typeStack.append("char")
    if p[-1] not in conTable.values():
        virtualMemory.check()
        conTable[virtualMemory.cCHAR] = p[-1]
        virtualMemory.cCHAR += 1
    else:
        pass

def p_verif(p):
    '''verif :'''
    exprOp = oStack.pop()
    idOp = oStack.pop()
    exprType = typeStack.pop()
    idType = typeStack.pop()
    if exprType == "int":
        if exprOp in conTable.values():
            quads.append([23, get_key(exprOp), get_key(functionDirectory[Passage.currentFunction].varTable[idOp].size), functionDirectory[Passage.currentFunction].varTable[idOp].dir])
            Passage.currentQuad += 1
            if idType == "int":
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pINT
                virtualMemory.pINT += 1  
            elif idType == "float":
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pFLOAT
                virtualMemory.pFLOAT += 1  
            else:
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pCHAR
                virtualMemory.pCHAR += 1  
            if functionDirectory[Passage.currentFunction].varTable[idOp].dir not in conTable.values():
                virtualMemory.check()
                conTable[virtualMemory.cINT] = functionDirectory[Passage.currentFunction].varTable[idOp].dir
                virtualMemory.cINT += 1  
            quads.append([1, get_key(functionDirectory[Passage.currentFunction].varTable[idOp].dir), get_key(exprOp), functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir])
            Passage.currentQuad += 1
            oStack.append("p%s" % Passage.currentPoint)
            typeStack.append(idType)
            Passage.currentPoint += 1
        else:
            quads.append([23, functionDirectory[Passage.currentFunction].varTable[exprOp].dir, get_key(functionDirectory[Passage.currentFunction].varTable[idOp].size), functionDirectory[Passage.currentFunction].varTable[idOp].dir])
            Passage.currentQuad += 1
            if idType == "int":
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pINT
                virtualMemory.pINT += 1  
            elif idType == "float":
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pFLOAT
                virtualMemory.pFLOAT += 1  
            else:
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint] = Var("pointer", Passage.currentScope)
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir = virtualMemory.pCHAR
                virtualMemory.pCHAR += 1  
            if functionDirectory[Passage.currentFunction].varTable[idOp].dir not in conTable.values():
                virtualMemory.check()
                conTable[virtualMemory.cINT] = functionDirectory[Passage.currentFunction].varTable[idOp].dir
                virtualMemory.cINT += 1  
            quads.append([1, get_key(functionDirectory[Passage.currentFunction].varTable[idOp].dir), functionDirectory[Passage.currentFunction].varTable[exprOp].dir, functionDirectory[Passage.currentFunction].varTable["p%s" % Passage.currentPoint].dir])
            Passage.currentQuad += 1
            oStack.append("p%s" % Passage.currentPoint)
            typeStack.append(idType)            
            Passage.currentPoint += 1
    else:
        print("Index used to call element in variable %s is not integer." % (idOp))
        sys.exit(0)

def p_call(p):
    '''call :'''
    if p[-1] in functionDirectory:
        oStack.append(p[-1])
        typeStack.append(functionDirectory[p[-1]].return_type)
        quads.append([20, -1, -1, functionDirectory[p[-1]].direction])
        Passage.currentQuad += 1
        Passage.paramCount = 1
        Passage.paramStatus = 1
        Passage.paramFun = p[-1]
    else:
        print("Unidentified function %s." % (p[-1]))
        sys.exit(0)

def p_pams(p):
    '''pams :'''
    if Passage.paramStatus == 1:
        rOp = oStack.pop()
        rType = typeStack.pop()
        if Passage.paramCount - 1 < len(functionDirectory[Passage.paramFun].signature):
            if (rType != functionDirectory[Passage.paramFun].signature[Passage.paramCount-1]):
                print("Invalid parameters on call to function %s." % Passage.paramFun)
                sys.exit(0)
            else:
                if rOp in conTable.values():
                    quads.append([21, get_key(rOp), -1, "p%s" % (Passage.paramCount)])
                else:
                    quads.append([21, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.paramFun].params[Passage.paramCount-1]])
                Passage.currentQuad += 1
                Passage.paramCount += 1
        else:
            print("Too many parameters in call to function %s." % (Passage.paramFun))
            sys.exit(0)
    else:
        pass

def p_confirm(p):
    '''confirm :'''
    if Passage.paramCount - 1 == len(functionDirectory[Passage.paramFun].signature):
        quads.append([22, -1, -1, functionDirectory[Passage.paramFun].direction])
        Passage.currentQuad += 1
        Passage.paramStatus = 0
        rOp = oStack.pop()
        rType = typeStack.pop()
        if rType != "void":
            if rType == "int":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("int", "temporal")
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tINT
                virtualMemory.tINT += 1
                functionDirectory[Passage.currentFunction].size[0] += 1
            elif rType == "float":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("float", "temporal")
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tFLOAT
                virtualMemory.tFLOAT += 1
                functionDirectory[Passage.currentFunction].size[1] += 1
            elif rType == "char":
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp] = Var("char", "temporal")
                virtualMemory.check()
                functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir = virtualMemory.tCHAR
                virtualMemory.tCHAR += 1
                functionDirectory[Passage.currentFunction].size[2] += 1
            quads.append([5, functionDirectory[Passage.currentFunction].varTable[rOp].dir, -1, functionDirectory[Passage.currentFunction].varTable["t%s" % Passage.currentTemp].dir])
            oStack.append("t%s" % Passage.currentTemp)
            typeStack.append(rType)
            Passage.currentQuad += 1
            Passage.currentTemp += 1
        else:
            pass
    else:
        print("Not enough arguments sent on call to function %s." % (Passage.paramFun))
        sys.exit(0)

def p_error(p):
    print("Syntax error on token %s" % (p.value))
    sys.exit(0)

parser = yacc.yacc()

parser.parse(Lexer.input)

quadN = 1

with open('OBJ.txt', 'w') as f:
    for key, value in functionDirectory.items():
        f.write('%s\n' % (key))

    f.write("#################")
    f.write("\n")

    for key, value in conTable.items(): 
        f.write("%s\n" % (value))

    f.write("#################")
        
    for item in quads:
        f.write("\n%d - %s" % (quadN, item))
        quadN += 1