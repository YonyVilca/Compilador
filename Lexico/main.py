import ply.lex as lex

reserved = {
    'entero': 'TIPO_ENTERO',
    'decimal': 'TIPO_DECIMAL',
    'caracter': 'TIPO_CARACTER',
    'booleano': 'TIPO_BOOLEANO',
    'cadena': 'TIPO_CADENA',
    'regresar': 'REGRESAR',
    'principal': 'PRINCIPAL',
    'si': 'SI',
    'sino': 'SINO',
    'para': 'PARA',
    'mientras': 'MIENTRAS',
    'hacer': 'HACER',
    'salida': 'SALIDA',
    'entrada': 'ENTRADA',
    'fin_linea': 'FIN_LINEA'
}

tokens = (
    'IDENTIFICADOR',
    'ENTERO',
    'DECIMAL',
    'CARACTER',
    'CADENA',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'MODULO',
    'IGUAL',
    'SUMA_IGUAL',
    'RESTA_IGUAL',
    'MULTIPLICACION_IGUAL',
    'DIVISION_IGUAL',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'PUNTO_COMA',
    'COMA',
    'PUNTO',
    'COMILLA_SIMPLE',
    'COMILLA_DOBLE',
    'MENOR_QUE',
    'MAYOR_QUE',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'DIFERENTE',
    'IGUAL_IGUAL',
    'Y_LOGICO',
    'O_LOGICO',
    'NEGACION',
    'INCREMENTO',
    'DECREMENTO',
    'COMENTARIO_LINEA',
    'COMENTARIO_BLOQUE',
) + tuple(reserved.values())

t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'\/'
t_MODULO = r'\%'
t_IGUAL = r'\='
t_SUMA_IGUAL = r'\+\='
t_RESTA_IGUAL = r'\-\='
t_MULTIPLICACION_IGUAL = r'\*\='
t_DIVISION_IGUAL = r'\/\='
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_PUNTO_COMA = r'\;'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_COMILLA_SIMPLE = r'\''
t_COMILLA_DOBLE = r'\"'
t_MENOR_QUE = r'\<'
t_MAYOR_QUE = r'\>'
t_MENOR_IGUAL = r'\<\='
t_MAYOR_IGUAL = r'\>\='
t_DIFERENTE = r'\!\='
t_IGUAL_IGUAL = r'\=\='
t_Y_LOGICO = r'\&\&'
t_O_LOGICO = r'\|\|'
t_NEGACION = r'\!'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'\-\-'
t_COMENTARIO_LINEA = r'\/\/.*'
t_COMENTARIO_BLOQUE = r'\/\*[\s\S]*?\*\/'

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CARACTER(t):
    r'\'([^\\\n]|(\\.))\''
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  

t_ignore = ' \t'

def t_error(t):
    token_dict = {
        'type': 'ILEGAL',
        'lexeme': t.value[0],
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    }
    print(token_dict)
    t.lexer.skip(1)

lexer = lex.lex()

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = (token.lexpos - last_cr)
    return column

f = open('Lexico/codigo.txt', 'r')
data = f.read()
lexer.input(data)

tokens_list = []

while True:
    tok = lexer.token()
    if not tok:
        break
    token_dict = {
        'type': tok.type,
        'lexeme': tok.value,
        'line': tok.lineno,
        'column': find_column(data, tok)
    }
    tokens_list.append(token_dict)

for token in tokens_list:
    print(token)