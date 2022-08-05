#Constructor de Instrucciones. Crea diccionarios con los diferentes tipos de valores
#que puedan necesitarse en ejecución.
from Recursos.TipoInstruccion import TIPO_INSTRUCCION

def operacion(_izquierda, _derecha, _tipo, _linea, _columna):
    return {
        'izquierda': _izquierda,
        'derecha': _derecha,
        'tipo': _tipo,
        'linea': _linea,
        'columna': _columna
    }

def valor(_valor, _tipo, _linea, _columna):
    return{
        'valor': _valor,
        'tipo': _tipo,
        'linea': _linea,
        'columna': _columna
    }
    
def casteo(_salida, _valor, _tipo, _linea, _columna):
    return{
        'salida': _salida,
        'valor': _valor,
        'tipo': _tipo,
        'linea': _linea,
        'columna': _columna
    }

def dmain(_instrucciones, _linea, _columna):
    return {
        'instrucciones': _instrucciones,
        'linea': _linea,
        'columna': _columna,
        'tipo': TIPO_INSTRUCCION['DMAIN']
    }

def println(_cadena, _valores, _linea, _columna):
    return {
        'tipo': TIPO_INSTRUCCION['PRINTLN'],
        'expresion': _cadena,
        'valores': _valores,
        'linea': _linea,
        'columna': _columna
    }

print(println(1,1,1,1))
    
    
