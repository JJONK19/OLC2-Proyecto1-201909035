from ply import lex, yacc
from Recursos.Errores.Error import error
from datetime import date

class Analizador:
    errores = []                    #Lista de errores
#-----------------------------------------------------------------------------------------

#                                    ANALISIS LEXICO

#-----------------------------------------------------------------------------------------
    states = (
        ('CADENA', 'exclusive')
    )

    reservadas = {
        'let' : 'LET', 
        'mut' : 'MUT',
        'true': 'TRUE',
        'false': 'FALSE',
        'Vec' : 'VEC',
        'vec' : 'vec',
        'new' : 'NEW',
        'struct' : 'STRUCT',
        'i64' : 'I64',
        'F64' : 'F64',
        'bool' : 'BOOL',
        'char' : 'CHAR',
        '&str' : '&STR',
        'String' : 'STRING',

    }

    tokens = reservadas + {
        'MAS', 'MENOS', 'MUL', 'DIV', 'PTOCOMA', 'ENTERO', 'FLOAT', 'ID', 'CHAR', 'CADENA', 'COMA',
        'CORA', 'CORC', 'DOSPTOS', 'MENOR', 'MAYOR', 'IGUAL', 'PARA', 'PARC', 'DDOSPTOS', 'ADMIC', 
        'LLAVA', 'LLAVC', 'Comentarios', 'SaltoLinea', 
    }

    t_ignore = ' \t'

    #Basado en: https://www.dabeaz.com/ply/ply.html#ply_nn3 Sección 4.3
    def t_ID(t):
        r'([a-zA-Z_])([a-zA-Z0-9_])*'
        t.type = Analizador.reservadas.get(t.value,'ID')    #Si no encuentra la key, el tipo es ID por defecto
        return t

    def t_ENTERO(t):
        r'[0-9]+'
        try:
            t.value = int(t.value)
        except:
            print('Error al parsear ENTERO')
            t.value = 0
        return t

    def t_FLOAT(t):
        r'[0-9]+("."[0-9]+)'
        try:
            t.value = float(t.value)
        except:
            print('Error al parsear FLOAT')
            t.value = 0
        return t

    t_MAS = r'\+'
    t_MENOS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_PTOCOMA = r';'
    t_CHAR = r'\'("\n"|"\\\\"|"\t"|"\r"|\\\'|\\\"|.)\''
    t_COMA = r','
    t_CORA = r'\['
    t_CORC = r'\]'
    t_LLAVA = r'}'
    t_LLAVC = r'{'
    t_PARA = r'\('
    t_PARC = r'\)'
    t_ADMIC = r'\!'
    t_DDOSPTOS = r'::'
    t_DOSPTOS = r':'
    t_MENOR = r'<'
    t_MAYOR = r'>'
    t_IGUAL = r'='



    #Reconocer y armar cadenas
    #Basado en: https://www.dabeaz.com/ply/ply.html#ply_nn3 Sección 4.19
    def t_CADENA (t):
        r'\"'        
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.begin('String')                 #Entra al estado que analiza cadenas
        return t

    def t_CADENA_ComillaDoble(t):     
        r'\\\"'
        return '\"'

    def t_CADENA_SaltoLinea(t):     
        r'\\n'
        return '\n'

    def t_CADENA_Espacio(t):     
        r'\s'
        return ' '

    def t_CADENA_Tab(t):     
        r'\\t'
        return '\t'

    def t_CADENA_Diagonal(t):     
        r'\\\\'
        return '\\'

    def t_CADENA_ComillaSimple(t):     
        r'\\\''
        return '\''

    def t_CADENA_Contenido(t):     
        r'[^"\\]+'
        
    def t_CADENA_Salir(t):     
        r'\"'
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')           
        return t

    #Comentarios
    def t_Comentarios(t):
        r'\/\/.*'
        pass

    #Saltos de Linea. Lex no maneja filas.
    def t_SaltoLinea(t):
        r'\n'
        t.lexer.lineno += 1
        return t

    #Manejo de Errores Lexicos
    def t_error(t):
        fecha = date.now()
        formato = fecha.strftime("%d/%m/%Y %H:%M")
        nuevoError = error('Lexico', 'Caracter Invalido:' + t.value[0], '', t.lexer.lineno, t.lexer.lexpos, formato)
        Analizador.errores.push(nuevoError)                        
        t.lexer.skip(1)

    lexer = lex.lex()

    #-----------------------------------------------------------------------------------------

    #                           ANALISIS SINTACTICO

    #-----------------------------------------------------------------------------------------

    precedence = (
        ('left','MAS','MENOS'),
        ('left','POR','DIVIDIDO')
    )

    parser = yacc.yacc()

    def analizar(cadena):
        return Analizador.parser.parse(cadena)