### Disenio de Lenguajes de Programacion
### Saul Contreras

import pickle
import lectorExpresionesMejorado
import traductorExpresion_a_AFD

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Funcion que nos va a permitir generar un automata AFD a partir de una expresion regular
def automata(tokensRegex, dictTokens, dictKeywords, whiteSpace):
    ### Iniciamos con las entradas de los tokens
    arbolExpresionRegularAFD, _, _ = lectorExpresionesMejorado.conversionExpresionRegular(tokensRegex)

    ###------------------------------------------AFD-DIRECTO----------------------------------------###
    ### Se hace una sustitucion previa para las expresiones 
    arbolNodosExpresionRegularSustituido = traductorExpresion_a_AFD.sustitucionPrevia(arbolExpresionRegularAFD)

    ### Se convierten los nodos que no son operandos en Nodos para almacenar
    ### Conjunto estados, transiciones, estado inicial, estado final
    ### Aqui el arbol ya esta en modo nodos para procesarse los nodos Complejos
    ### Las correspondencias las tendremos guardadas para referencias de la construccion de subconjuntos
    arbolNodosExpresionRegularAFD, _, correspondencias = traductorExpresion_a_AFD.traduccionBase(arbolNodosExpresionRegularSustituido, 1, [])

    ### Obtenemos los nodos hojas que ya poseen sus posiciones
    nodosHoja = traductorExpresion_a_AFD.devolverNodosHoja(arbolNodosExpresionRegularAFD, [])

    ### Se realiza la definicion de nodos que no son hojas con sus operaciones nullable, firstpos, lastpos
    nodoRoot, nodos = traductorExpresion_a_AFD.definirNodosAFD(arbolNodosExpresionRegularAFD, 0, [])

    ### Unimos los nodos en un solo arreglo
    nodosFinales = nodosHoja + nodos

    ### Se calcula la tabla de followpos con los nodosFinales resultantes
    tablaFollowpos = traductorExpresion_a_AFD.followpos(nodosFinales, correspondencias)

    ### Obtener el conjunto de simbolos
    simbolos = traductorExpresion_a_AFD.simbolosAFDDirecta(correspondencias)

    ### Obtener las transiciones y estados (el primer estado es el estado inicial)
    dStatesAFD, dTransAFD  = traductorExpresion_a_AFD.traduccionAFDDirecta(nodoRoot, simbolos, tablaFollowpos, correspondencias)

    posicionesFinales = []

    ### Posicion para determinar que estados son finales
    for correspondencia in correspondencias:
        if correspondencia[0] == '#':
            posicionesFinales.append(correspondencia[1])

    ### Creamos una estructura de Nodo para simular el AFD
    afdd = traductorExpresion_a_AFD.convertirAFDDirectaNodo(dStatesAFD, dTransAFD, simbolos, posicionesFinales)

    ### Serializar afdd con Pickle
    with open('Pickle/automata.pickle', 'wb') as f:
        pickle.dump(afdd, f)

    ### Serializar diccionario de Tokens con Pickle
    with open('Pickle/tokens.pickle', 'wb') as f:
        pickle.dump(dictTokens, f)

    ### Serializar diccionario de Keywords con Pickle
    with open('Pickle/keywords.pickle', 'wb') as f:
        pickle.dump(dictKeywords, f)

    ### Serializar Set de Ignore con Pickle
    with open('Pickle/ignore.pickle', 'wb') as f:
        pickle.dump(whiteSpace, f)

    ### Escribir el scanner
    linea = '''### Disenio de Lenguajes de Programacion
### Saul Contreras
import sys
import random
import copy
import pickle
import lectorExpresionesMejorado
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

IGNORE = 'IGNORE'

### Lectura de pickle del Automata Serializado
with open('Pickle/automata.pickle', 'rb') as f:
    afdd = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('Pickle/tokens.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('Pickle/keywords.pickle', 'rb') as f:
    keywords = pickle.load(f)

### Lectura de pickle de la definicion de IGNORE Serializado
with open('Pickle/ignore.pickle', 'rb') as f:
    ignoreSet = pickle.load(f)

### De aqui en adelante vamos a hacer la codificacion del Scanner
### Para la lectura de los tokens

### Primero leemos el archivo a modo de obtener una sola linea
fileName = sys.argv[1]
fileTxt = open(fileName, 'r', encoding='utf-8')
stringValidar = ''.join(fileTxt.readlines())
stringValidarAscii = ''
tokensList = []
#print(tokens)

### Ahora pasamos el string a la simulacion
posicion = 0
while posicion < len(stringValidar):
    token, posicion, cadenaRetornar = simulaciones.simulacionAFD2(afdd, stringValidar, posicion, tokens, ignoreSet)

    ### Se limpia la cadena a retornar de los ignores
    cadenaFinal = ''
    for caracter in cadenaRetornar:
        if ignoreSet:
            caracterAscii = ord(caracter)
            if caracterAscii in ignoreSet:
                continue
        cadenaFinal = cadenaFinal + caracter

    if token:
        ### Se obtiene el valor de la bandera del token
        valorToken = tokens[token]
        valorBandera = valorToken[1]

        ### Revisar el valor de la bandera
        if (valorBandera == 1) and (cadenaFinal in keywords.values()):
            ### Imprimir que el string si es un KEYWORD
            #print('KEYWORD =>', cadenaFinal)
            llave = [key for key, value in keywords.items() if value == cadenaFinal]
            tokensList.append([llave[0], cadenaFinal])
        else:
            #print(token,'=>', cadenaFinal)
            tokensList.append([token, cadenaFinal])
    else:
        #print(f"Error Léxico: Token no esperado en la posicion: {repr(posicion)} con el valor {repr(cadenaFinal)}")
        pass
    
### Serializar tokens del scanner con Pickle
with open('Pickle/tokensScanner.pickle', 'wb') as f:
    for i in tokensList:
        print('type: \t', i[0], 'value : \t', i[1])
    pickle.dump(tokensList, f)'''

    archivo = open("scanner.py", "w")
    archivo.write(linea)
    archivo.close()

    print("""

The scanner has been written >>> scanner.py 

    use: python3 scanner.py <File dir>

            """)

### Clase para alamacenar la estructura de un TOKEN
class Token():
    def __init__(self, attr, value):
        self.Atributo = attr
        self.Valor = value

### CODIGO DE ESTE PUNTO PARA ABAJO BASADO EN EJEMPLO https://www.geeksforgeeks.org/expression-evaluation/
### Funcion para calcular el primero de la produccion
def calculate_first(ident, primerosProducciones):
    if ident in primerosProducciones.keys():
        return primerosProducciones[ident]
    else:
        return [ident]

### Funcion para obtener el primero de la produccion
def get_first(left, right, operator, primerosProducciones):
    if operator == 'concat':
        if left.Atributo == 'ident':
            return calculate_first(left.Valor, primerosProducciones)
        elif right.Atributo == 'ident':
            return calculate_first(right.Valor, primerosProducciones)
        else:
            return []
    elif operator == 'union':
        return calculate_first(left.Valor, primerosProducciones) + calculate_first(right.Valor, primerosProducciones)

### Funcion para obtener el primer elemento de un stack
def peek(stack):
    return stack[-1] if stack else None

### Funcion para determinar si un elemento es un simbolo
def is_symbol(simbolo):
    tokens = ['ident', 'attr', 's_action', 'string', 'white']
    if simbolo.Atributo in tokens:
        return True
    return False

### Funcion para aplicar un operador entre nodos
def apply_operator(operators, values, primerosProduccion, tabs):
    operator = operators.pop()

    if len(values) == 1 and operator.Atributo == 'br_close':
        right = ([], [])
    else:
        right = values.pop()

    if len(values) == 0:
        left = ([], [])
    else:
        left = values.pop()
    
    if operator.Atributo == 'union':
        resultado, tabs = operator_or(left, right, tabs, primerosProduccion)
        return resultado, tabs
    elif operator.Atributo == 'concat':
        resultado, tabs = operator_concat(left, right, tabs, primerosProduccion)
        return resultado, tabs
    elif operator.Atributo == 'br_open':
        resultado, tabs = operator_llave(left, right, tabs, primerosProduccion)
        return resultado, tabs
    elif operator.Atributo == 'br_close':
        resultado, tabs = operator_llave_cerrada(left, right, tabs, primerosProduccion)
        return resultado, tabs
    elif operator.Atributo == 'sq_open':
        resultado, tabs = operator_corchete(left, right, tabs, primerosProduccion)
        return resultado, tabs
    elif operator.Atributo == 'sq_close':
        resultado, tabs = operator_corchete_cerrado(left, right, tabs, primerosProduccion)
        return resultado, tabs

### Funcion para obtener los nodos a partir de un signo "["
def operator_corchete(left, right, tabs, primerosProduccion):
    operator = 'square'
    first = root = []

    if isinstance(left, tuple):
        root = left[0]
    else:
        tabs = tabs - 1
        if left.Atributo == 's_action':
            root = ['\t' * tabs + left.Valor[2:-2]]
        elif left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = root + ['\t' * tabs + '\tself.' + left.Valor + '()']
            tabs = tabs + 1
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            #root = root + ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + 'self.expect("' + left.Valor + '")']

    if isinstance(right, tuple):
        tabs = tabs - 1
        root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(right[1]) + ':'] + ['\t' + i for i in right[0]]
    else:
        root = root + ['\t' * tabs + 'self.expect("' + right.Valor + '")']
    return (root, first), tabs

### Funcion para obtener los nodos a partir de un signo "]"
def operator_corchete_cerrado(left, right, tabs, primerosProduccion):
    operator = 'square close'
    first = []
    tabs = tabs - 1

    # RIGHT
    if isinstance(right, tuple):
        root = left[0] + right[0]
    else:
        root = left[0]
        if right.Atributo == 's_action':
            root = root + ['\t' * tabs + right.Valor[2:-2]]
        elif right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            #root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[right.Valor])]
            root = root + ['\t' * tabs +  'self.' + right.Valor + '()']
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            #root = root + ['\t' * tabs + 'if self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + 'self.expect("' + right.Valor + '")']

    return (root, first), tabs

### Funcion para obtener los nodos a partir de un signo "{"
def operator_llave(left, right, tabs, primerosProduccion):
    operator = 'kleene'
    first = []
    root = []

    if isinstance(left, tuple):
        root = left[0]
    else:
        tabs = tabs - 1
        if left.Atributo == 's_action':
            root = ['\t' * tabs + left.Valor[2:-2]]
        elif left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = ['\t' * tabs + '\tself.' + left.Valor + '()']
            tabs = tabs + 1
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            #root = root + ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + 'self.expect("' + left.Valor + '")']
        tabs = tabs + 1

    if isinstance(right, tuple):
        tabs = tabs - 2
        root = root + ['\t' * tabs + 'while self.currentToken in ' + repr(right[1]) + ':'] + ['\t' + i for i in right[0]]
        tabs = tabs + 1
    else:
        root = root + ['\t' * tabs + 'self.expect("' + right.Valor + '")']
    return (root, first), tabs

### Funcion para obtener los nodos a partir de un signo "}"
def operator_llave_cerrada(left, right, tabs, primerosProduccion):
    operator = 'kleene close'
    first = []
    tabs = tabs - 1

    # RIGHT
    if isinstance(right, tuple):
        root = left[0] + right[0]
    else:
        root = left[0]
        if right.Atributo == 's_action':
            root = root + ['\t' * tabs + right.Valor[2:-2]]
        elif right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[right.Valor]) + ':']
            root = root + ['\t' * tabs +  '\tself.' + right.Valor + '()']
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            #root = root + ['\t' * tabs + 'if self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + 'self.expect("' + right.Valor + '")']

    return (root, first), tabs

### Funcion para obtener los nodos a partir de un signo "|"
def operator_or(left, right, tabs, primerosProduccion):
    operator = 'union'
    
    if isinstance(left, tuple) and isinstance(right, tuple):
        tabs = tabs - 1
        root = left[0] + ['else:'] + right[0]
        tabs = tabs - 1
        return (root, left[1] + right[1]), tabs

    elif not isinstance(left, tuple) and not isinstance(right, tuple):
        root = []
        first = get_first(left, right, operator, primerosProduccion)

        # LEFT
        if left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = root + ['\t' * tabs +  '\tself.' + right.Valor + '()']
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + left.Valor + '")']

        # RIGHT
        if right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'elif self.currentToken in ' + repr(primerosProduccion[right.Valor]) + ':']
            root = root + ['\t' * tabs +  '\tself.' + right.Valor + '()']
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'elif self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + right.Valor + '")']
                    
        tabs = tabs - 1
        return (root, first), tabs

    elif isinstance(left, tuple) and not isinstance(right, tuple):
        root = left[0] + ['else:']
        first = left[1]

        # RIGHT
        if right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[right.Valor]) + ":"]
            root = root + ['\t' * tabs +  '\tself.' + right.Valor + '()']
            first = first + primerosProduccion[right.Valor]
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + right.Valor + '")']
            first = first + [right.Valor]

        tabs = tabs - 1
        return (root, first), tabs

    elif not isinstance(left, tuple) and isinstance(right, tuple):
        root = []
        first = right[1]
        tabs = tabs - 1

        # LEFT
        if left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = root + ['\t' * tabs +  '\tself.' + left.Valor + '()']
            first = first + primerosProduccion[left.Valor]
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + left.Valor + '")']
            first = first + [left.Valor]

        root = root + ['else:'] + ['\t' + r for r in right[0]]

        tabs = tabs - 1
        return (root, first), tabs

### Funcion para obtener los nodos a partir de un signo "."
def operator_concat(left, right, tabs, primerosProduccion):
    operator = 'concat'
    first = []
    if isinstance(left, tuple) and isinstance(right, tuple):
        root = left[0] + right[0]
        first = left[1]
        return (root, first), tabs

    elif not isinstance(left, tuple) and not isinstance(right, tuple):
        root = []

        first = get_first(left, right, operator, primerosProduccion)
        # LEFT
        if left.Atributo == 's_action':
            root = root + ['\t' * tabs + left.Valor[2:-2]]
        elif left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = root + ['\t' * tabs + '\tself.' + left.Valor + '()']
            tabs = tabs + 1
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + left.Valor + '")']
            tabs = tabs + 1

        # RIGHT
        if right.Atributo == 's_action':
            root = root + ['\t' * tabs + right.Valor[2:-2]]
        elif right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'self.' + right.Valor + '()']
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + right.Valor + '")']
            tabs = tabs + 1
        elif right.Atributo == 'attr':
            x = root[-1][:-2].rfind('\t')
            root[-1] = root[-1][:-2][:x + 1] + right.Valor[1:-1] + ' = ' + root[-1][:-2][x + 1:] + '(' + right.Valor[1:-1] + ')'

        return (root, first), tabs

    elif isinstance(left, tuple) and not isinstance(right, tuple):
        root = left[0]
        first = left[1]

        # RIGHT
        if right.Atributo == 's_action':
            root = root + ['\t' * tabs + right.Valor[2:-2]]
        elif right.Atributo == 'ident' and right.Valor in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'self.' + right.Valor + '()']
        elif right.Atributo == 'ident' and right.Valor not in primerosProduccion.keys():
            root = root + ['\t' * tabs + 'if self.currentToken == "' + right.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + right.Valor + '")']
            tabs = tabs + 1
        elif right.Atributo == 'attr':
            x = root[-1][:-2].rfind('\t')
            root[-1] = root[-1][:-2][:x + 1] + right.Valor[1:-1] + ' = ' + root[-1][:-2][x + 1:] + '(' + right.Valor[1:-1] + ')'

        return (root, first), tabs
    
    elif not isinstance(left, tuple) and isinstance(right, tuple):
        root = right[0]

        # LEFT
        if left.Atributo == 's_action':
            root = ['\t' * tabs + left.Valor[2:-2]] + root
            first = right[1]
        elif left.Atributo == 'ident' and left.Valor in primerosProduccion.keys():
            root = ['\t' * tabs + 'if self.currentToken in ' + repr(primerosProduccion[left.Valor]) + ':']
            root = root + ['\t' * tabs + '\tself.' + left.Valor + '()'] + right[0]
            tabs = tabs + 1
            first = calculate_first(left.Valor, primerosProduccion)
        elif left.Atributo == 'ident' and left.Valor not in primerosProduccion.keys():
            root = ['\t' * tabs + 'if self.currentToken == "' + left.Valor + '":']
            root = root + ['\t' * tabs + '\tself.expect("' + left.Valor + '")'] + right[0]
            first = [left.Valor]
            tabs = tabs + 1
        return (root, first), tabs

### Funcion para determinar la precedencia de simbolos
def greater_precedence(op1, op2):
    precedences = {
        'union' : 2,
        'concat' : 3,
        'br_open' : 1,
        'br_close': 0,
        'sq_open' : 1,
        'sq_close': 0
    }
    return precedences[op1] >= precedences[op2]
    
### Clase para procesar el arbol sintactico de una produccion dada en tokens
def constructorArbol(tokensProduccion, primerosProducciones):
    ### Estructura del Arbol
    root = None
    nodos = []
    simbolos = []
    ids = 0
    tabs = 0

    ### Se hace una concatenacion de los tokens de la produccion
    tokensProductionProcess = []
    operators = ['{', '|','(', '[', '}', ']', ')']
    contador = 0

    for contador in range(len(tokensProduccion)):
        if contador + 1 >= len(tokensProduccion):
            tokensProductionProcess.append(tokensProduccion[-1])
            break

        tokensProductionProcess.append(tokensProduccion[contador])

        if tokensProduccion[contador].Valor == '}' and tokensProduccion[contador + 1].Valor in '({[]}':
            tokensProductionProcess.append(Token('concat', '.'))
        elif tokensProduccion[contador].Valor not in operators and tokensProduccion[contador+1].Valor not in operators:
            tokensProductionProcess.append(Token('concat', '.'))
        elif tokensProduccion[contador].Valor not in operators and tokensProduccion[contador+1].Valor in '([':
            tokensProductionProcess.append(Token('concat', '.'))
        elif tokensProduccion[contador].Valor == ')' and tokensProduccion[contador+1].Valor not in operators:
            tokensProductionProcess.append(Token('concat', '.'))

    tokensProduccion = tokensProductionProcess

    ### Se procesa el ARBOL SINTACTICO
    values = []
    operators = []
    for token in tokensProduccion:
        if is_symbol(token):
            values.append(token)

        elif token.Atributo == 'p_open':
            operators.append(token)

        elif token.Atributo == 'p_close':
            top = peek(operators)

            while top is not None and top.Atributo != 'p_open':
                raiz, tabs = apply_operator(operators, values, primerosProducciones, tabs)
                values.append(raiz)
                top = peek(operators)
            operators.pop()
            tabs = tabs - 1

        else:
            top = peek(operators)

            while top is not None and top.Atributo not in ['p_open', 'p_close'] and greater_precedence(top.Atributo, token.Atributo):
                raiz, tabs = apply_operator(operators, values, primerosProducciones, tabs)
                values.append(raiz)
                top = peek(operators)
            operators.append(token)
        
    while peek(operators) is not None:
        raiz, tabs = apply_operator(operators, values, primerosProducciones, tabs)
        values.append(raiz)

    ### Se obtiene la estructura de codigo hacia la raiz
    root = values.pop()
    return root
