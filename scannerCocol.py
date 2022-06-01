### Disenio de Lenguajes de Programacion
### Saul Contreras
import pickle

import lectorExpresionesMejorado
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

IGNORE = 'IGNORE'

### Lectura de pickle del Automata Serializado
with open('Pickle/automataCocol.pickle', 'rb') as f:
    afdd = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('Pickle/tokensCocol.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('Pickle/keywordsCocol.pickle', 'rb') as f:
    keywords = pickle.load(f)

### Lectura de pickle de la definicion de IGNORE Serializado
with open('Pickle/ignoreCocol.pickle', 'rb') as f:
    ignoreSet = pickle.load(f)

### De aqui en adelante vamos a hacer la codificacion del Scanner
### Para la lectura de los tokens

### Primero leemos el archivo a modo de obtener una sola linea
fileName = input("Ingrese el nombre de su archivo a validar: ")
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
            tokensList.append([llave, cadenaFinal])
        else:
            #print(token,'=>', cadenaFinal)
            tokensList.append([token, cadenaFinal])
    else:
        #print('Error Lexico =>', cadenaFinal)
        pass

print("-----------------------")
print(tokensList)