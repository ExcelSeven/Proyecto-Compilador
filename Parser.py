import ply.yacc as yacc     # Import PLU yacc module
import Lexer                # Import my lexer information
tokens = Lexer.tokens

# Set-up of operator precendence
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# Dictionary of names
names = { }

# Formal Grammar
def p_program_structure(p):
    '''program_structure : PROGRAM NAME SEMI declare_var full_fun MAIN LPAREN RPAREN LCURLY statutes RCURLY'''

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR''' 

def p_declare_var(p):
    '''declare_var : VARS type COLON multivars SEMI'''

def p_multivars(p):
    '''multivars : NAME 
                 | NAME COMMA multivars
                 | dimvars
                 | dimvars COMMA multivars'''

def p_dimvars(p):
    '''dimvars : NAME dimensions'''

def p_dimensions(p):
    '''dimensions : LBRACK expr RBRACK
                  | LBRACK expr RBRACK dimensions'''

def p_declare_fun(p):
    '''declare_fun : FUNCTION return_type NAME LPAREN type COLON multivars RPAREN'''

def p_return_type(p):
    '''return_type : INT
                    | FLOAT
                    | CHAR
                    | VOID'''

def p_full_fun(p):
    '''full_fun : declare_fun declare_var LCURLY statutes RCURLY
                | declare_fun declare_var LCURLY statutes RCURLY full_fun'''

def p_statutes(p):
    '''statutes : assign
                | assign statutes
                | call
                | call statutes
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

def p_param(p):
    '''param : type COLON NAME
             | type COLON NAME COMMA param'''

def p_assign(p):
    '''assign : NAME EQUALS expr'''

def p_call(p):
    '''call : NAME LPAREN exprs RPAREN'''

def p_returning(p):
    '''returning : RETURN LPAREN expr RPAREN SEMI'''

def p_reading(p):
    '''reading : READ LPAREN multivars RPAREN SEMI'''

def p_writing(p):
    '''writing : WRITE LPAREN write_opt RPAREN SEMI'''

def p_write_opt(p):
    '''write_opt : QUOTE MESSAGE QUOTE
                 | QUOTE MESSAGE QUOTE write_opt
                 | exprs
                 | exprs write_opt'''

def p_decision(p):
    '''decision : IF LPAREN expr RPAREN THEN LCURLY statutes SEMI RCURLY ELSE LCURLY statutes SEMI RCURLY'''

def p_conditional(p):
    '''conditional : WHILE LPAREN expr RPAREN DO LCURLY statutes SEMI RCURLY'''

def p_nonconditional(p):
    '''nonconditional : FOR expr EQUALS expr TO expr DO LCURLY statutes SEMI RCURLY'''

def p_exprs(p):
    '''exprs : expr
             | expr COMMA exprs'''

def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | term'''

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''

def p_factor(p):
    '''factor : NUMBER
              | NAME
              | dimvars
              | NAME LPAREN exprs RPAREN'''

yacc.yacc()