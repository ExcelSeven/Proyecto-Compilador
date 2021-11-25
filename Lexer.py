import ply.lex as lex   

reserved = {
    'program'   : 'PROGRAM', 
    'main'      : 'MAIN', 
    'vars'      : 'VARS', 
    'int'       : 'INT', 
    'float'     : 'FLOAT', 
    'char'      : 'CHAR', 
    'void'      : 'VOID', 
    'function'  : 'FUNCTION', 
    'return'    : 'RETURN', 
    'read'      : 'READ', 
    'write'     : 'WRITE', 
    'if'        : 'IF', 
    'then'      : 'THEN', 
    'else'      : 'ELSE', 
    'while'     : 'WHILE', 
    'do'        : 'DO', 
    'for'       : 'FOR', 
    'to'        : 'TO',
    'media'     : 'MEDIA',
    'moda'      : 'MODA',
    'varianza'  : 'VARIANZA',
    'regresion' : 'REGRESION',
    'plot'      : 'PLOT'
}

tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COMPARE', 'DIFFERENT', 'AND', 'OR', 'LESSER', 'GREATER', 'LPAREN', 'RPAREN', 'LCURLY', 
         'RCURLY', 'LBRACK', 'RBRACK', 'SEMI', 'COLON', 'COMMA', 'LESSER_EQ', 'GREATER_EQ', 'ID', 'C_INT', 'C_FLOAT', 'C_CHAR', 'MESSAGE']

tokens = tokens + list(reserved.values())

t_PLUS       = r'\+'
t_MINUS      = r'\-'
t_TIMES      = r'\*'
t_DIVIDE     = r'\/'
t_EQUALS     = r'='
t_COMPARE    = r'=='
t_DIFFERENT  = r"!="
t_AND        = r'\&'
t_OR         = r'\|'
t_LESSER     = r'<'
t_GREATER    = r'>'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LCURLY     = r'\{'
t_RCURLY     = r'\}'
t_LBRACK     = r'\['
t_RBRACK     = r'\]'
t_SEMI       = r'\;'
t_COLON      = r'\:'
t_COMMA      = r'\,'
t_LESSER_EQ  = r'<='
t_GREATER_EQ = r'>='

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')   
     return t

def t_C_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    return t

def t_C_INT(t):
    r'[0-9]+'
    return t

def t_C_CHAR(t):
    r'''['][a-zA-Z][']'''
    return t

def t_MESSAGE(t):
    r'["][^\n]+["]'
    return t

t_ignore    = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

Op = input("Which test to run?: ")

f = open("./testcase%s.txt" % Op, "r")
input = f.read()
