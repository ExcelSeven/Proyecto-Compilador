import ply.yacc as yacc     # Import PLU yacc module
import Lexer                # Import my lexer information

tokens = Lexer.tokens

# Formal Grammar
def p_program_structure(p):
    '''program_structure : PROGRAM ID SEMI declare_var functions MAIN LPAREN RPAREN LCURLY statutes RCURLY'''

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR''' 

def p_declare_var(p):
    '''declare_var : VARS type COLON multivars SEMI'''

def p_multivars(p):
    '''multivars : ID 
                 | ID COMMA multivars
                 | dimvars
                 | dimvars COMMA multivars'''

def p_dimvars(p):
    '''dimvars : ID dimensions'''

def p_dimensions(p):
    '''dimensions : LBRACK expr RBRACK
                  | LBRACK expr RBRACK dimensions'''

def p_declare_fun(p):
    '''declare_fun : FUNCTION return_type ID LPAREN RPAREN
                   | FUNCTION return_type ID LPAREN params RPAREN'''

def p_return_type(p):
    '''return_type : INT
                    | FLOAT
                    | CHAR
                    | VOID'''

def p_functions(p):
    '''functions : declare_fun declare_var LCURLY statutes RCURLY
                 | declare_fun declare_var LCURLY statutes RCURLY functions'''

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

def p_params(p):
    '''params : type COLON multivars
              | type COLON multivars SEMI params'''

def p_assign(p):
    '''assign : ID EQUALS expr SEMI
              | dimvars EQUALS expr SEMI'''

def p_call_void(p):
    '''call_void : ID LPAREN exprs RPAREN SEMI'''

def p_returning(p):
    '''returning : RETURN LPAREN expr RPAREN SEMI'''

def p_reading(p):
    '''reading : READ LPAREN multivars RPAREN SEMI'''

def p_writing(p):
    '''writing : WRITE LPAREN write_opt RPAREN SEMI'''

def p_write_opt(p):
    '''write_opt : QUOTE MESSAGE QUOTE
                 | QUOTE MESSAGE QUOTE COMMA write_opt
                 | exprs
                 | exprs COMMA write_opt'''

def p_decision(p):
    '''decision : IF LPAREN logic RPAREN THEN LCURLY statutes SEMI RCURLY 
                | IF LPAREN logic RPAREN THEN LCURLY statutes SEMI RCURLY ELSE LCURLY statutes SEMI RCURLY'''

def p_conditional(p):
    '''conditional : WHILE LPAREN logic RPAREN DO LCURLY statutes SEMI RCURLY'''

def p_nonconditional(p):
    '''nonconditional : FOR expr EQUALS expr TO expr DO LCURLY statutes SEMI RCURLY'''

def p_relation(p):
    '''relation : expr GREATER expr
                | expr GREATER_EQ expr
                | expr LESSER expr
                | expr LESSER_EQ expr
                | expr COMPARE expr'''

def p_logic(p):
    '''logic : relation AND relation
             | relation OR relation
             | relation'''

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
    '''factor : C_INT
              | MINUS C_INT
              | C_FLOAT
              | MINUS C_FLOAT
              | C_CHAR
              | ID
              | dimvars
              | ID LPAREN exprs RPAREN'''

parser = yacc.yacc()
