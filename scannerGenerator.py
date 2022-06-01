### Disenio de Lenguajes de Programacion
### Saul Contreras

import bridge
import sys
import copy
import pickle
import simulaciones

### Definicion de constantes
STRING = 'string'
COMPILER = 'COMPILER'
BEGINCOMMENT = '(.'
ENDCOMMENT = '.)'
END = 'END'
CHARACTERS = 'CHARACTERS'
KEYWORDS = 'KEYWORDS'
TOKENS = 'TOKENS'
PRODUCTIONS = 'PRODUCTIONS'
IGNORE = 'IGNORE'
COMILLAS = '"'
PLUS = '+'
MINUS = '-'
DOT = '.'
UNTIL = '..'
ANY = 'ANY'
EXCEPTKEYWORDS = 'EXCEPT KEYWORDS'

anySet = set()
for i in range(9, 128):
    anySet.add(i)
    anySet.add(241)
    anySet.add(209)

def compilerHeader(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(COMPILER):
        return linea.split(COMPILER,1)[1]

    return None

def compilerEnd(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(END):
        return linea.split(END,1)[1]

    return None

def whiteSpaceIgnore(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(IGNORE):
        return linea.split(IGNORE,1)[1]

    return None

def isBeginComment(linea):
    comentario = ''
    linea = linea.strip()
    if linea.startswith(BEGINCOMMENT):
        return True, linea.split(BEGINCOMMENT,1)[1]

    return None, comentario

def isEndComment(linea):
    comentario = ''
    linea = linea.strip()
    if linea.endswith(ENDCOMMENT):
        return True, linea.split(ENDCOMMENT,1)[0]

    return None, comentario

def processCharacter(setCharacter, dictCharacters):
    setCharacter = setCharacter[:-1]
    setCharacter = setCharacter.replace("'", '"')

    comillas = 0
    saltos = None
    signo = None
    set1 = set()
    set2 = set()
    palabra1 = ''
    palabra2 = ''

    for i in range(len(setCharacter)):
        if not saltos:
            if setCharacter[i] == COMILLAS:
                comillas = comillas + 1
                continue
        
            if comillas % 2 == 0:
                if (setCharacter[i] == PLUS) or (setCharacter[i] == MINUS) or ((setCharacter[i] == '.') and (setCharacter[i+1] == '.')):
                    if signo:
                        if (len(set1) == 0) and (len(set2) == 0):
                            set1 = dictCharacters[palabra1]
                            set2 = dictCharacters[palabra2]

                            palabra1 = ''
                            palabra2 = ''
                        elif (len(set1) == 0):
                            set1 = dictCharacters[palabra1]
                            palabra1 = ''
                        elif (len(set2) == 0):
                            set2 = dictCharacters[palabra2]
                            palabra2 = ''
                        else:
                            pass

                        if signo == PLUS:
                            set1 = set1.union(set2)
                        elif signo == MINUS:
                            set1 = set1.difference(set2)
                        else:
                            s1 = list(set1)
                            s2 = list(set2)

                            set1 = set()
                            for k in range(int(s1[0]), int(s2[0])+1):
                                set1.add(k)

                        set2 = set()
                        signo = None
                    if (setCharacter[i] == '.') and (setCharacter[i+1] == '.'):
                        saltos = 1
                        signo = UNTIL
                    else:
                        signo = setCharacter[i]
                    continue
                
                if (setCharacter[i] == 'C') and (setCharacter[i+1] == 'H') and (setCharacter[i+2] == 'R') and (setCharacter[i+3] == '('):
                    saltos = 3
                    for j in range(0,len(setCharacter)-i-4):
                        saltos = saltos + 1
                        if setCharacter[i+j+4] == ')':
                            caracter = setCharacter[i+4:i+j+4]

                            if caracter:
                                if signo:
                                    set2.add(int(caracter))
                                else:
                                    set1.add(int(caracter))
                            break
                
                else:
                    if signo:
                        palabra2 = palabra2 + setCharacter[i]
                    else:
                        palabra1 = palabra1 + setCharacter[i]

            else:
                if signo:
                    set2.add(ord(setCharacter[i]))
                else:
                    set1.add(ord(setCharacter[i]))
        else:
            saltos = saltos - 1    

    if signo:
        if (len(set1) == 0) and (len(set2) == 0):
            set1 = dictCharacters[palabra1]
            set2 = dictCharacters[palabra2]
        elif (len(set1) == 0):
            set1 = dictCharacters[palabra1]
        elif (len(set2) == 0):
            set2 = dictCharacters[palabra2]
        else:
            pass

        if signo == PLUS:
            set1 = set1.union(set2)
        elif signo == MINUS:
            set1 = set1.difference(set2)
        else:
            s1 = list(set1)
            s2 = list(set2)

            set1 = set()
            for k in range(int(s1[0]), int(s2[0])+1):
                set1.add(k)
        set2 = set()
        signo = None

    if (len(set1) == 0) and (len(palabra1) != 0):
        set1 = dictCharacters[palabra1]

    return set1

def processToken(setTokens, dictCharacters):
    bandera = 0

    comillas = 0
    saltos = None
    expresionRegular = ''

    if EXCEPTKEYWORDS in setTokens:
        bandera = 1
        setTokens = setTokens.replace(EXCEPTKEYWORDS, '').strip()

    for i in range(len(setTokens)):
        if not saltos:
            if setTokens[i] == COMILLAS:
                comillas = comillas + 1
                continue

            if comillas % 2 == 0:
                if COMILLAS in setTokens[i:]:
                    indice = setTokens[i:].index('"')
                    saltos = indice - 1

                    tokenReplace = setTokens[i:indice + i]

                else:
                    saltos = len(setTokens[i:])
                    tokenReplace = setTokens[i:]

                tokenReplaceDict = tokenReplace.replace('{', '(').replace('}', ')*').replace('[', '(').replace(']', ')?')

                for key in sorted(dictCharacters, key=len, reverse=True):
                    if key in tokenReplaceDict:
                        preRegex = ''
                        for value in dictCharacters[key]:
                            preRegex = preRegex + str(value) + '|'

                        tokenReplaceDict = tokenReplaceDict.replace(key, '(' + preRegex[:-1] + ')')

                expresionRegular = expresionRegular + tokenReplaceDict

            else:
                expresionRegular = expresionRegular + str(ord(setTokens[i]))

        else:
            saltos = saltos - 1

    return expresionRegular, bandera

def tokenizacionProducciones(producciones):
    listaProducciones = []

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

    ### Se revisa cada una de las producciones
    for produccion in producciones:
        tokensList = []

        ### Ahora pasamos el string a la simulacion
        posicion = 0
        while posicion < len(produccion):
            token, posicion, cadenaRetornar = simulaciones.simulacionAFD2(afdd, produccion, posicion, tokens, ignoreSet)

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
                    llave = [key for key, value in keywords.items() if value == cadenaFinal]
                    tokensList.append([llave[0], cadenaFinal])
                else:
                    tokensList.append([token, cadenaFinal])
            else:
                pass

        ### Se elimina el primer elemento que es el IDENTIFICADOR de la PRODUCCION
        tokenCopy = copy.deepcopy(tokensList)

        ### Se genera el diccionario de la PRODUCCION
        #diccionarioProducciones[tokensList[0][1]] = tokenCopy
        for token in tokenCopy:
            listaProducciones.append((token[0], token[1]))

    ### Se devuelven las PRODUCCIONES
    return listaProducciones

###-------------------------MAIN---------------------------###
### Se solicita el nombre del archivo
fileName = sys.argv[1]

### Se extraen las lineas del archivo que se leera
archivo = open(fileName, 'r', encoding='utf-8')
lineas = archivo.readlines()

identCompiler = None
identEndCompiler = None
thereIsBeginCommet = None
thereIsEndCommet = None
readCharacters = None
readKeywords = None
readTokens = None
readProductions = None
readWhitespace = None

dictCharacters = {}
dictKeywords = {}
dictTokens = {}
dictProductions = {}
listProductions = []
whiteSpace = None

pilaComentario = ''
lineaAnterior = ''
contador = 0

### Agregamos la definicion de ANY a los CHARACTERS
dictCharacters[ANY] = anySet

### Se va haciendo una lectura del archivo linea por linea
for linea in lineas:
    ### Si aun no tenemos el header COMPILER con el ident lo buscamos hasta encontrarlo
    if not identCompiler:
        ### Primero se busca que lo primero en el archivo sea el header con COMPILER ident
        identCompiler = compilerHeader(linea)
        if identCompiler:
            identCompiler = identCompiler.strip()
        continue

    ### Si ya tenemos el header COMPILER con el ident buscamos END ident
    if identCompiler:
        ### Primero se busca que lo primero en el archivo sea el header con COMPILER ident
        identEndCompiler = compilerEnd(linea)
        if identEndCompiler:
            identEndCompiler = identEndCompiler.strip()

        if identEndCompiler:
            if identEndCompiler[-1] != DOT:
                identEndCompiler = identEndCompiler + DOT

            if (identEndCompiler[:-1] == identCompiler):
                break
            elif (identEndCompiler[:-1] != identCompiler):
                print("Error de identificador de COMPILER")
                exit()

    ### Una vez tenemos el COMPILER ident se procede a revisar comentarios
    if not thereIsBeginCommet:
        thereIsBeginCommet, pilaComentario = isBeginComment(linea)
        if thereIsBeginCommet:
            comentario = ''
            thereIsEndCommet, comentario = isEndComment(linea)

            if thereIsEndCommet:
                pilaComentario = pilaComentario + '\n' + comentario
                thereIsBeginCommet = False
                thereIsEndCommet = False

                ### Se muestran los comentarios del archivo en pantalla
                #print(pilaComentario)
            else:
                pilaComentario = pilaComentario + '\n' + linea
            
            continue

    ### Si se inicio un comentario, solo hay que imprimir hasta que termine el comentario
    if thereIsBeginCommet:
        ### Siempre se busca el final del comentario para seguir procesando el resto del archivo
        ### que no esta dentro de los comentarios
        comentario = ''
        thereIsEndCommet, comentario = isEndComment(linea)

        if thereIsEndCommet:
            pilaComentario = pilaComentario + '\n' + comentario
            thereIsBeginCommet = False
            thereIsEndCommet = False

            ### Se muestran los comentarios del archivo en pantalla
            #print(pilaComentario)
        else:
            pilaComentario = pilaComentario + '\n' + linea
        
        continue
    
    ### Si no hay un inicio de comentario se procede a revisar la estructura de COCOR
    if linea.strip() == CHARACTERS:
        readCharacters = True
        readKeywords = False
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == KEYWORDS:
        readCharacters = False
        readKeywords = True
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == TOKENS:
        readCharacters = False
        readKeywords = False
        readTokens = True
        readProductions = False
        continue
    elif linea.strip() == PRODUCTIONS:
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = True
        continue
    elif whiteSpaceIgnore(linea.strip()) != None:
        whiteSpace = whiteSpaceIgnore(linea.strip()).strip()

        ### Revisar si el whiteSpace corresponde a un SET
        whiteSpace = whiteSpace.strip().replace("' '", 'CHR(32)').replace(' ', '')
        whiteSpace = whiteSpace.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if whiteSpace[-1] != DOT:
            whiteSpace = whiteSpace + '.'

        ### Procesar el SET
        whiteSpace = processCharacter(whiteSpace, dictCharacters)

        ### Determinar que no se esta leyendo CHARACTERS, TOKENS, KEYWORDS, ni PRODUCTIONS
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = False
        continue


    ### Revisar si la linea esta vacia y continuar
    if linea.strip() == '':
        continue

    ### Concatenar linea anterior
    linea = lineaAnterior + linea.strip('\n').strip('\t').strip()

    contador = contador + 1


    ### Si estoy leyendo CHARACTERS los proceso como corresponde
    if readCharacters:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionCharacter = linea.partition('=')
        identCharacter = particionCharacter[0].strip()
        setCharacter = particionCharacter[2].strip().replace("' '", 'CHR(32)').replace(' ', '')
        setCharacter = setCharacter.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setCharacter[-1] == DOT:
            lineaAnterior = ''

            ### Procesar el SET
            setCharacter = processCharacter(setCharacter, dictCharacters)

            ### Conjutos de CHARACTERS a almacenar (Se van a volver string separador por OR cuando se sutituyan en el TOKEN)
            dictCharacters[identCharacter] = setCharacter

        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    ### Si estoy leyendo KETWORDS los proceso como corresponde
    if readKeywords:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionKeywords = linea.partition('=')
        identKeyword = particionKeywords[0].strip().replace(' ', '')
        setKeyword = particionKeywords[2].strip().replace('"', '').replace("' '", 'CHR(32)').replace(' ', '')
        setKeyword = setKeyword.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setKeyword[-1] == DOT:
            lineaAnterior = ''
            dictKeywords[identKeyword] = setKeyword[:-1]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue
    ### Si estoy leyendo TOKENS los proceso como corresponde
    if readTokens:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionTokens = linea.partition('=')
        identTokens = particionTokens[0].strip()
        setTokens = particionTokens[2].strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setTokens[-1] == DOT:
            lineaAnterior = ''

            ### Procesar el TokenExpr a una expresion regular
            expresionRegular, bandera = processToken(setTokens[:-1], dictCharacters)

            dictTokens[identTokens] = [expresionRegular, bandera]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    ### Si estoy leyendo PRODUCTIONS los proceso como corresponde
    if readProductions:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue
        
        listProductions.append(linea.strip('\n').strip('\t').strip().replace('\t', ''))
        lineaAnterior = ''

### Revisamos lo obtenido
# print(dictCharacters)
# print(dictKeywords)
# print(dictTokens)
# print(listProductions)
# print(whiteSpace)

### Hacer uso del proyecto 2 para obtener las PRODUCCIONES como TOKENS
if listProductions:
    dictProductions = tokenizacionProducciones(listProductions)
    
    ### Serializar las producciones con Pickle
    with open('Pickle/productions.pickle', 'wb') as f:
        pickle.dump(dictProductions, f)

    contador = 1
    ### Agregar tokens de tipo string a los tokens
    for produccion in dictProductions:
        if produccion[0] == STRING:
            ### Procesar el TokenExpr a una expresion regular
            expresionRegular, bandera = processToken(produccion[1], dictCharacters)

            nombreToken = 'token' + str(contador)

            if [expresionRegular, bandera] not in dictTokens.values():
                dictTokens[nombreToken] = [expresionRegular, bandera]
                contador = contador + 1

### Se contruye una unica expresion regular con los tokens
expresion = ''
for regex in dictTokens.values():
    expresion = expresion + '(' + regex[0] + ')#|'

expresion = expresion[:-1]

### Mandamos a llamar al bridge para que construya el Scanner con la expresion formada a partir de Tokens
bridge.automata(expresion, dictTokens, dictKeywords, whiteSpace)
