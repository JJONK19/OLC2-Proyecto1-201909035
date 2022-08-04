from asyncio.windows_events import NULL
from ply import lex, yacc
from Recursos.Errores.Error import error
from Recursos.Instruccion import Instruccion
from Recursos.Enum.TipoDato import TIPO_DATO
from Recursos.Enum.TipoValor import TIPO_VALOR
from Recursos.Enum.TipoOperacion import TIPO_OPERACION
from datetime import date

class Analizador:
    errores = []                    #Lista de errores
    instrucciones = []              #Lista de instrucciones
    simbolos = []                   #Lista de simbolos
    metodos = []                    #Lista de metodos

#-----------------------------------------------------------------------------------------

#                                    ANALISIS LEXICO

#-----------------------------------------------------------------------------------------
    states = (
        ('cadena', 'exclusive')
    )

    reservadas = {
        'let' : 'let', 
        'mut' : 'mut',
        'true': 'true',
        'false': 'false',
        'Vec' : 'Vec',
        'vec' : 'vec',
        'new' : 'new',
        'struct' : 'struct',
        'i64' : 'i64',
        'f64' : 'f64',
        'bool' : 'bool',
        'char' : 'char',
        '&str' : 'str',
        'pow' : 'pow',
        'powF' : 'powF',
        'as' : 'as',
        'String' : 'string'
    }

    tokens = reservadas + {
        'mas', 'menos', 'mul', 'div', 'ptocoma', 'entero', 'float', 'id', 'char', 'cadena', 'coma',
        'corA', 'corC', 'dosptos', 'menor', 'mayor', 'igual', 'parA', 'parC', 'ddosptos', 'not', 
        'llavA', 'llavC', 'mod', 'or', 'and' 'Comentarios', 'SaltoLinea', 
    }

    t_ignore = ' \t'

    #Basado en: https://www.dabeaz.com/ply/ply.html#ply_nn3 Sección 4.3
    def t_id(t):
        r'([a-zA-Z_])([a-zA-Z0-9_])*'
        t.type = Analizador.reservadas.get(t.value,'id')    #Si no encuentra la key, el tipo es ID por defecto
        return t

    def t_entero(t):
        r'[0-9]+'
        try:
            t.value = int(t.value)
        except:
            print('Error al parsear ENTERO')
            t.value = 0
        return t

    def t_float(t):
        r'[0-9]+("."[0-9]+)'
        try:
            t.value = float(t.value)
        except:
            print('Error al parsear FLOAT')
            t.value = 0
        return t

    t_mas = r'\+'
    t_menos = r'-'
    t_mul = r'\*'
    t_div = r'/'
    t_igual = r'%'
    t_ptocoma = r';'
    t_char = r'\'("\n"|"\\\\"|"\t"|"\r"|\\\'|\\\"|.)\''
    t_coma = r','
    t_corA = r'\['
    t_corC = r'\]'
    t_llavA = r'}'
    t_llavC = r'{'
    t_parA = r'\('
    t_parC = r'\)'
    t_ddosptos = r'::'
    t_dosptos = r':'
    t_menorIgual = r'<='
    t_mayorIgual = r'>='
    t_menor = r'<'
    t_mayor = r'>'
    t_igual = r'=='
    t_asignacion = r'='
    t_desigual = r'!='
    t_and = r'&&'
    t_or = r'\|\|' 
    t_not = r'!'


    #Reconocer y armar cadenas
    #Basado en: https://www.dabeaz.com/ply/ply.html#ply_nn3 Sección 4.19
    def t_cadena (t):
        r'\"'        
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.begin('String')                 #Entra al estado que analiza cadenas
        return t

    def t_cadena_ComillaDoble(t):     
        r'\\\"'
        return '\"'

    def t_cadena_SaltoLinea(t):     
        r'\\n'
        return '\n'

    def t_cadena_Espacio(t):     
        r'\s'
        return ' '

    def t_cadena_Tab(t):     
        r'\\t'
        return '\t'

    def t_cadena_Diagonal(t):     
        r'\\\\'
        return '\\'

    def t_cadena_ComillaSimple(t):     
        r'\\\''
        return '\''

    def t_cadena_Contenido(t):     
        r'[^"\\]+'
        
    def t_cadena_Salir(t):     
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
        ('right', 'asignacion'),
        ('left', 'or'),
        ('left', 'and'),
        ('left', 'menor', 'menorIgual', 'mayor', 'mayorIgual'),
        ('left', 'igual', 'desigual'),
        ('left','mas','menos'),
        ('left','mul','div', 'mod'),
        ('right', 'not'),
        ('right', 'umenos')
    )

    def p_INICIO(t):
        '''INICIO : SENTENCIAS
        '''
        t[0] = {
            'Errores' : Analizador.errores,
            'Instrucciones' : Analizador.instrucciones,
            'Metodos' : Analizador.metodos,
            'Simbolos' : Analizador.simbolos
        }
        Analizador.errores = []
        Analizador.instrucciones = []
        Analizador.metodos = []
        Analizador.simbolos = []

    def p_SENTENCIAS(t):
        '''SENTENCIAS : SENTENCIAS SENTENCIA 
                      | SENTENCIA
        '''
        if(len(t) == 3):
            t[1].push(t[2])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_SENTENCIA(t):
        '''SENTENCIA : EXPRESION 
        '''
        t[0] = t[1]

    #Tipos-------------------------------------------------------------------------------------------
    def p_TIPO_I64(t):
        '''TIPO : i64
        '''
        t[0] = TIPO_DATO["I64"]

    def p_TIPO_F64(t):
        '''TIPO : f64
        '''
        t[0] = TIPO_DATO["F64"]

    def p_TIPO_BOOL(t):
        '''TIPO : bool
        '''
        t[0] = TIPO_DATO["BOOL"]
    
    def p_TIPO_CHAR(t):
        '''TIPO : char
        '''
        t[0] = TIPO_DATO["CHAR"]
    
    def p_TIPO_STR(t):
        '''TIPO : str
        '''
        t[0] = TIPO_DATO["STR"]

    def p_TIPO_STRING(t):
        '''TIPO : string
        '''
        t[0] = TIPO_DATO["STRING"]

    #Expresiones-------------------------------------------------------------------------------------
    def p_EXPRESION_SUMA(t):
        '''EXPRESION : EXPRESION mas EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["SUMA"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_RESTA(t):
        '''EXPRESION : EXPRESION menos EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["RESTA"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_MULTIPLICACION(t):
        '''EXPRESION : EXPRESION mul EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MULTIPLICACION"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_DIVISION(t):
        '''EXPRESION : EXPRESION div EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["DIVISION"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_MOD(t):
        '''EXPRESION : EXPRESION mod EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MODULO"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_POTENCIAI(t):
        '''EXPRESION :  i64 ddosptos pow parA EXPRESION coma EXPRESION parC
        '''
        t[0] = Instruccion.operacion(t[5], t[7], TIPO_OPERACION["POTENCIAI"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_POTENCIAF(t):
        '''EXPRESION :  f64 ddosptos powf parA EXPRESION coma EXPRESION parC
        '''
        t[0] = Instruccion.operacion(t[5], t[7], TIPO_OPERACION["POTENCIAF"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_NEGATIVO(t):
        '''EXPRESION :  menos EXPRESION %prec umenos
        '''
        t[0] = Instruccion.operacion(t[2], None, TIPO_OPERACION["UNARIO"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_PARENTESIS(t):
        '''EXPRESION :  parA EXPRESION parC
        '''
        t[0] = t[2]

    def p_EXPRESION_IGUAL(t):
        '''EXPRESION :  EXPRESION igual EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["IGUAL"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_DESIGUAL(t):
        '''EXPRESION :  EXPRESION desigual EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["DESIGUAL"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_MENOR(t):
        '''EXPRESION :  EXPRESION menor EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MENOR"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_MENORIGUAL(t):
        '''EXPRESION :  EXPRESION menorIgual EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MENORIGUAL"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_MAYOR(t):
        '''EXPRESION :  EXPRESION mayor EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MENOR"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_MAYORIGUAL(t):
        '''EXPRESION :  EXPRESION mayorIgual EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["MAYORIGUAL"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_OR(t):
        '''EXPRESION :  EXPRESION or EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["OR"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_AND(t):
        '''EXPRESION :  EXPRESION and EXPRESION
        '''
        t[0] = Instruccion.operacion(t[1], t[3], TIPO_OPERACION["AND"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_NOT(t):
        '''EXPRESION :  not  EXPRESION
        '''
        t[0] = Instruccion.operacion(t[2], None, TIPO_OPERACION["NOT"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_ENTERO(t):
        '''EXPRESION :  entero
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["I64"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_FLOAT(t):
        '''EXPRESION :  float
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["F64"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_TRUE(t):
        '''EXPRESION :  true
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["BOOL"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_FALSE(t):
        '''EXPRESION :  false
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["BOOL"], t.lineno(1), t.lexpos(1))
    
    def p_EXPRESION_TEXTO(t):
        '''EXPRESION : cadena
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["STR"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_CHAR(t):
        '''EXPRESION :  char
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["CHAR"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_ID(t):
        '''EXPRESION :  id
        '''
        t[0] = Instruccion.valor(t[1], TIPO_VALOR["ID"], t.lineno(1), t.lexpos(1))

    def p_EXPRESION_CASTEO(t):
        '''EXPRESION : EXPRESION as TIPO
        '''
        t[0] = Instruccion.casteo(t[3], t[1], TIPO_OPERACION["CASTEO"], t.lineno(1), t.lexpos(1))

    #Errores Sintaxis--------------------------------------------------------------------------------
    def p_error(t):
        fecha = date.now()
        formato = fecha.strftime("%d/%m/%Y %H:%M")
        nuevoError = error('Sintáctico', 'Token Inesperado:' + t.value, '', t.lineno, t.lexpos, formato)
        Analizador.errores.push(nuevoError)

        #Verficar que el archivo no ha acabado
        if not t:
            return
 
        while True:
            nextToken = Analizador.parser.token()            
            if not nextToken or nextToken.type == 'PTOCOMA': 
                break
        Analizador.parser.restart()

    parser = yacc.yacc()

    def analizar(cadena):
        return Analizador.parser.parse(cadena)