### Disenio de Lenguajes de Programacion
### Saul Contreras

### Programa parserContructor que permite la creacion del programa Parser
import pickle
import utils
import copy

### Constantes
espaciadoIndent = '    '

### Funcion para calcular primero de cada PRODUCCION
def primerosProduccion(tokensProduccion, noTerminalesList, dictPrimero):
    primeroProduccion = []
    parentesisSimbolo = False
    corcheteSimbolo = False
    tokenIdent = False

    ### Se revisan los token de la produccion para revisar la estructura 
    ### Y determinar cuando se tiene mas de un FIRST
    for tokenProduccion in tokensProduccion:
        token, value = [*tokenProduccion]

        ### Revision de cierre de parentesis en token
        if token == 'p_close':
            parentesisSimbolo = False
            break

        ### Revision de cierre de corchetes en token
        elif token == 'sq_close':
            corcheteSimbolo = False

        ### Se revisa si existe un parentesis haciendo scope
        if parentesisSimbolo:
            ### Se revisa si existe un token de una union
            if tokenIdent:
                if token == 'union':
                    tokenIdent = False
            else:
                ### Se revisa si el token es un ident No Terminal
                if token == 'ident' and value in noTerminalesList and value in dictPrimero:
                    tokenIdent = True
                    primeroProduccion = primeroProduccion + dictPrimero[value]
                ### Se revisa si el token es un ident Terminal
                elif token == 'ident' and value not in noTerminalesList:
                    tokenIdent = True
                    primeroProduccion.append(value)
                ### Se revisa si el token es un string siendo este un TERMINAL
                elif token == 'string':
                    tokenIdent = True
                    primeroProduccion.append(value.replace('"', ''))

        ### Se revisa si existe un corchete haciendo scope
        elif corcheteSimbolo:
            ### Se revisa si el token es un ident No Terminal
            if token == 'ident' and value in noTerminalesList:
                primeroProduccion = primeroProduccion + dictPrimero[value]
            ### Se revisa si el token es un ident Terminal
            elif token == 'ident' and value not in noTerminalesList:
                primeroProduccion.append(value)
            ### Se revisa si el token es un string siendo este un TERMINAL
            elif token == 'string':
                primeroProduccion.append(value.replace('"', ''))

        ### Si los token no tienen agrupacion se revisa directamente
        ### Se revisa si el token es un ident No Terminal
        elif token == 'ident' and value in noTerminalesList:
            primeroProduccion = primeroProduccion + dictPrimero[value]
            break
        ### Se revisa si el token es un ident Terminal
        elif token == 'ident' and value not in noTerminalesList:
            primeroProduccion.append(value)
            break
        ### Se revisa si el token es un string siendo este un TERMINAL
        elif token == 'string':
            primeroProduccion.append(value.replace('"', ''))
            break

        ### Se revisa si hay una apertura de Parentesis
        if token == 'p_open':
            parentesisSimbolo = True
        ### Se revisa si hay una apertura de Corchetes
        elif token == 'sq_open':
            corcheteSimbolo = True

    return primeroProduccion

### Funcion para poder construir el parser
def contruirParser(productionsTokens, productionsList, dictPrimero, tokensExtras, contadorExtras, codigoParser):
    ### Se inicializan las variables para poder procesar las funciones con el ARBOL SINTACTICO
    palabrasNoTeminales = []
    funciones = []
    argumentos = []
    elementosProduccion = []

    ### Se obtienen los No Terminales de las producciones
    validador = True
    listaCopy = copy.deepcopy(productionsTokens)
    primerValor = listaCopy.pop(0)
    tok, valor = [*primerValor]
    
    ### Obtenemos el primero de los No Terminales
    palabrasNoTeminales.append(valor)

    ### Se itera sobre los tokens de la produccion
    ### Buscando el token que esta despues de un token p_end
    ### Que es el NO TERMINAL
    for i in listaCopy:
        if validador:
            tok, valor = [*i]
            if tok == 'p_end':
                validador = False
        else:
            tok, valor = [*i]
            palabrasNoTeminales.append(valor)
            validador = True

    ### Se obtienen los argumentos de las funciones de los NO TERMINALES
    ### Y se obtiene el resto de los tokens que conforman los elementos
    ### de la produccion
    for token in productionsTokens:
        t, v = [*token]
        if t == 'p_end':
            productionsList.append(funciones)

            for i in range(len(funciones)):
                if funciones[i][1] == '=':
                    if len(funciones[:i]) == 2:
                        argumentos.append(funciones[1:i])
                    else:
                        argumentos.append([])
                    elementosProduccion.append(funciones[i + 1:])
                    break
            funciones = []
        else:
            funciones.append(token)

    ### Se comienza con el primer NO TERMINAL que es nuestro Simbolo Inicial
    codigoParser = codigoParser + 'self.' + palabrasNoTeminales[0] + '()'

    ### Se obtienen los tokens que vienen dentro de la produccion como Strings
    nuevosTokenString = {}
    for i, item in enumerate(elementosProduccion):
        for index, exp in enumerate(item):
            if exp[0] == 'string':
                exprSimple = exp[1][1:-1]
                if exprSimple not in nuevosTokenString.keys():
                    name = 'token' + str(contadorExtras)
                    nuevosTokenString[exprSimple] = name
                    contadorExtras = contadorExtras + 1

                elementosProduccion[i][index] = ('ident', nuevosTokenString[exprSimple])

    ### Se obtienen los tokens que vienen como Strings en las producciones
    tokensExtras = {}
    for ident, value in nuevosTokenString.items():
        tokensExtras[ident] = value

    ### Se calculan los primeros elementos de cada produccion
    for i in range(len(elementosProduccion) - 1, 0, -1):
        listaPrimeros = primerosProduccion(elementosProduccion[i], palabrasNoTeminales, dictPrimero)
        noterminal1 = palabrasNoTeminales[i]
        dictPrimero[noterminal1] = listaPrimeros


    ### Convertir los Tokens de producciones a una Estructura TOKENS
    ### Construir el Arbol a partir de los TOKENS de la PRODUCCION
    for i in range(len(palabrasNoTeminales)):
        tokensProduccion = []
        ### Conversion a estructura TOKEN
        for j in elementosProduccion[i]:
            t = utils.Token(j[0], j[1])
            tokensProduccion.append(t)
        ### Procesamiento de los TOKENS para formal el ARBOL
        raiz = utils.constructorArbol(tokensProduccion, dictPrimero)

        ### Procesamiento de los argumentos a funcion
        argumentosFuncion = ''
        if len(argumentos[i]) > 0:
            for argumentoLocal in argumentos[i]:
                argumentosFuncion = ', ' + argumentoLocal[1][1:-1]

        ### Espaciado de la primer linea de la funcion 
        codigoParser = codigoParser + '\n\n' + espaciadoIndent
        ### Definicion de la funcion con argumentos
        codigoParser = codigoParser + 'def ' + palabrasNoTeminales[i] + '(self' + argumentosFuncion + '):\n'
        ### Contruccion de la funcion con los datos del arbol
        codigoParser = codigoParser + espaciadoIndent*2 + '\n        '.join(raiz[0])

    ### Se agrega la lectura de los tokens leidos por el Scanner para que los procese el parser generado
    codigoParser = codigoParser + '''\n\n### Lectura de pickle del Automata Serializado
with open('Pickle/tokensScanner.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Correr el Parser
parser = Parser(tokens)

parser.parser()'''

    f = open('parserProgram.py', 'w', encoding='utf-8')
    f.write(codigoParser)
    f.close()

### Lectura de pickle de la definicion de PRODUCTIONS Serializado
with open('Pickle/productions.pickle', 'rb') as f:
    productionsTokens = pickle.load(f)
    

### Variables para nuestro programa
productionsList = []
dictPrimero = {}
tokensExtras = {}
contadorExtras = 1
codigoParser = '''
### Disenio de Lenguajes de Programacion
### Saul Contreras
### Carnet 18409

import pickle

### Clase Parser creada a partir del arbol sintactico    
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.currentToken = None
        self.lastvalue = None

        self.nextToken = self.tokens[self.posicion]
        self.get()

        self.parser()

    def error(self, reporte):
        print(reporte)

    def expect(self, terminal):
        if self.currentToken == terminal:
            self.get()
        elif(self.currentToken != None and terminal!=None and terminal!='white'):
            print('Sintax error: Expected value is ' + self.currentToken + ', Actual value is: ' + terminal)

    def get(self):
        if self.posicion - 1 < 0:
            self.lastvalue = None
        else:
            self.lastvalue = self.tokens[self.posicion - 1][1]

        if self.nextToken == None:
            self.currentToken = None
        else:
            self.currentToken = self.nextToken[0]
        self.posicion = self.posicion + 1

        if self.posicion >= len(self.tokens):
            self.nextToken = None
        else:
            self.nextToken = self.tokens[self.posicion]

    def parser(self):
        '''

### Se contruye el Parser
contruirParser(productionsTokens, productionsList, dictPrimero, tokensExtras, contadorExtras, codigoParser)

print("""

The Parser has been written """)