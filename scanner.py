### Disenio de Lenguajes de Programacion
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
        print('type: 	', i[0], 'value : 	', i[1])
    pickle.dump(tokensList, f)