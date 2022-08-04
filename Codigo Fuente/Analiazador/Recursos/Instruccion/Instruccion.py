#Constructor de Instrucciones. Crea diccionarios con los diferentes tipos de valores
#que puedan necesitarse en ejecución.

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
    