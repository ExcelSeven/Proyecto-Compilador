import ply.lex as lex   # Import PLY lex module
tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COMPARE', 'AND', 'OR', 'LESSER', 'GREATER', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'LBRACK', 'RBRACK', 'SEMI', 'COLON', 'COMMA', 'QUOTE', 
           'NAME', 'MESSAGE', 'NUMBER', 'PROGRAM', 'MAIN', 'VARS', 'INT', 'FLOAT', 'CHAR', 'VOID', 'FUNCTION', 'RETURN', 'READ', 'WRITE', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR', 'TO')

# Token definitions 
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_TIMES     = r'\*'
t_DIVIDE    = r'\/'
t_EQUALS    = r'\='
t_COMPARE   = r"=="
t_AND       = r'\&'
t_OR        = r'\|'
t_LESSER    = r'\<'
t_GREATER   = r'\>'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LBRACK    = r'\['
t_RBRACK    = r'\]'
t_SEMI      = r'\;'
t_COLON     = r'\:'
t_COMMA     = r'\,'
t_QUOTE     = r'\"'
t_NAME      = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_MESSAGE   = r'[a-zA-Z0-9_]*'
t_PROGRAM   = r"Program"
t_MAIN      = r"main"
t_VARS      = r"VARS"
t_INT       = r"int"
t_FLOAT     = r"float"
t_CHAR      = r"char"
t_VOID      = r"void"
t_FUNCTION  = r"function"
t_RETURN    = r"return"
t_READ      = r"read"
t_WRITE     = r"write"
t_IF        = r"if"
t_THEN      = r"then"
t_ELSE      = r"else"
t_WHILE     = r"while"
t_DO        = r"do"
t_FOR       = r"for"
t_TO        = r"to"

def t_NUMBER(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore    = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()