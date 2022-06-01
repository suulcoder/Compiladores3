### Programa que permite la traduccion de una expresion dada en estructura de listas (arbol) a un AFD en forma de Nodo (Forma Directa)

### Se importan librerias para
### - Copy: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
import copy

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Funcion que permite determinar si un caracter es un operador
def is_op(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False

### Funcion que permite contruir un AFD para el OR
def orAFD(nodos, nodo2):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    nodo.transicionOrAFD(nodos[0], nodo2)

    return nodo

### Funcion que permite contruir un AFD para la CONCATENCION
def concatAFD(nodos, nodo2):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    nodo.transicionConcatAFD(nodos[0], nodo2)

    return nodo

### Funcion que permite contruir un AFD para la cerradura KLEEN
def cerraduraAFD(nodos):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    nodo.transicionCerraduraAFD(nodos[0])

    return nodo

### Funcion que permite sustituir las expresiones de ? y + por sus equivalencias
def sustitucionPrevia(expresion):
    for nodo in range(len(expresion)):
        if type(expresion[nodo]) == list:
            sustitucionPrevia(expresion[nodo])
        else:
            ### Revisar si es un nodo que no es un operador
            if is_op(expresion[nodo]):
                ### Si es un operador hay que ver si se debe sustituir + y ?
                if expresion[nodo] == '?':
                    expresion.pop()
                    nodoAnterior = expresion.pop()
                    expresion.append(copy.deepcopy(nodoAnterior))
                    expresion.append('|')
                    expresion.append('ε')
                elif expresion[nodo] == '+':
                    expresion.pop()
                    nodoAnterior = expresion.pop()
                    expresion.append([copy.deepcopy(nodoAnterior), '*'])
                    expresion.append(copy.deepcopy(nodoAnterior))

    return expresion

### Funcion que permite tomar una expresion en forma de listas (arbol) y reemplazar los caracteres por Nodos AFD's Base
def traduccionBase(expresion, correlat, correspondencias):
    correlativo = correlat
    
    ### Por cada nodo en la expresion
    for nodo in range(len(expresion)):
        ### Si el elemento es otra lista, llamamos recursivamente al metodo
        if type(expresion[nodo]) == list:
            _, correlativo, _ = traduccionBase(expresion[nodo], correlativo, correspondencias)
        ### En caso el elemento sea un caracter
        else:
            ### Revisar si es un nodo que no es un operador
            if not is_op(expresion[nodo]):
                ### Si es un caracter vamos a crear el nodo y reemplazarlo en el arreglo original
                nuevoNodo = Nodo(expresion[nodo])
                correlativo = nuevoNodo.operacionesBase(correlativo)
                expresion[nodo] = nuevoNodo
                ### Guardar la corrspondencia de posicion a simbolo
                if nuevoNodo.exp != 'ε':
                    correspondencias.append([nuevoNodo.exp, correlativo - 1])

    ### Se devuelve la expresion con los nodos reemplazados y un correlativo para los estados siguientes en la construccion, y tambien las correspondencia de Nodo y posicion
    return expresion, correlativo, correspondencias

### Funcion que nos permite obtener los nodos Hoja de la expresion en forma de listas (arbol)
def devolverNodosHoja(expresionNodos, nodosHoj):
    nodosHoja = nodosHoj

    ### Recorremos la expresion
    for nodo in expresionNodos:
        ### Si el elemento es otra lista, llamamos recursivamente al metodo
        if type(nodo) == list:
            devolverNodosHoja(nodo, nodosHoja)
        ### Si no es una lista entonces...
        else:
            ### Revisar si es un nodo que no es un operador
            if not is_op(nodo):
                nodosHoja.append(nodo)

    ### Devolver los nodos Hoja
    return nodosHoja

### Funcion para generar los nodos operaciones del AFD
def definirNodosAFD(expresion, contadorExp, nodosProcess):
    contadorNodos = contadorExp
    nodosProcesados = nodosProcess
    nodos = []
    operador = ''

    ### Se itera sobre los elementos de la expresion
    for nodo in range(len(expresion)):
        ### Si es una lista entonces hay que hacer el proceso recursivo
        if type(expresion[nodo]) == list:
            nodo, _ = definirNodosAFD(expresion[nodo], 0, nodosProcesados)

            ### Revisamos la info previa al nodo para revisar si hay que hacer alguna operacion con el nodo devuelto
            if contadorNodos > 0:
                if contadorNodos > 0 and contadorNodos < 2 and operador != '|':
                    ### Vamos a crear un Nodo Concat y lo guardamos en nodosProcesados y agregar a nodos
                    nodoNuevo = concatAFD(nodos, nodo)
                    nodosProcesados.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1

                elif contadorNodos > 0 and contadorNodos < 2 and operador == '|':
                    ### Vamos a crear un Nodo OR y lo guardamos en nodosProcesados y agregar a nodos
                    nodoNuevo = orAFD(nodos, nodo)
                    nodosProcesados.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1
                    operador = ''
            else:
                ### Guardamos el nodo si no hay con que operar, agregar a nodos
                nodos.append(nodo)
                contadorNodos = contadorNodos + 1
        else:
            ### Si es un nodo o un operador hay que guardar el nodo, o guardar la expresion, u operar si ya es posible con
            ### los nodos almacenados y el operador
            if contadorNodos > 0:
                if (expresion[nodo] == '*') and contadorNodos == 1:
                    ### Guardamos el nodo como un * y agregamos a nodosProcesados
                    if expresion[nodo] == '*':
                        nodoNuevo = cerraduraAFD(nodos)
                        nodosProcesados.append(nodoNuevo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1
                elif not is_op(expresion[nodo]) and (contadorNodos < 2 and contadorNodos > 0)  and operador != '|':
                    ### Vamos a crear un Nodo Concat y lo guardamos en nodosProcesados y agregar a nodos
                    nodoNuevo = concatAFD(nodos, expresion[nodo])
                    nodosProcesados.append(nodoNuevo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1
                else:
                    ### Vamos a revisar si ya podemos operar el OR
                    if not is_op(expresion[nodo]) and (contadorNodos < 2 and contadorNodos > 0) and operador == '|':
                        ### Vamos a crear un Nodo OR y lo guardamos en nodosProcesados y agregar a nodos
                        nodoNuevo= orAFD(nodos, expresion[nodo])
                        nodosProcesados.append(nodoNuevo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1
                        operador = ''
                    else:
                        ### Guardamos el operador | entre los nodos y agregamos la cantidad de nodos
                        operador = '|'
            else:
                ### Guardamos en nodos y tambien en nodosProcesados
                nodos.append(expresion[nodo])
                contadorNodos = contadorNodos + 1

    ### Se devuelve el Nodo raiz y los nodos que se generaron en la construccion del nodo Raiz
    return nodos[0], nodosProcesados

### Funcion para construir la tabla de Followpos dados los nodos utilizados y las posiciones inciales
def followpos(nodos, posiciones):
    tablaFollowpos = {}

    ### Obtenemos las posiciones para la tabla followpos
    for posicion in posiciones:
        tablaFollowpos[posicion[1]] = []

    ### Iteramos sobre los nodos
    for nodo in nodos:
        ### Si el nodo es una CONCATENACION o KLEEN procedemos
        if (nodo.tipoNodo == '.') or (nodo.tipoNodo == '*'):
            ### Si es un KLEEN obtenemos followpos segun la regla 
            if nodo.tipoNodo == '*':
                for pos in nodo.lastpos:
                    for posi in nodo.firstpos:
                        tablaFollowpos[pos].append(posi)
            ### Si es una CONCATENACION obtenemos followpos segun la regla 
            elif nodo.tipoNodo == '.':
                c1 = nodo.hijos[0]
                c2 = nodo.hijos[1]
                for pos in c1.lastpos:
                    for posi in c2.firstpos:
                        tablaFollowpos[pos].append(posi)

    ### Limpiar la tabla para crear conjuntos sin elementos repetidos
    for key in tablaFollowpos:
        tablaFollowpos[key] = list(dict.fromkeys(tablaFollowpos[key]))

    ### Se devuelve la tabla Followpos
    return tablaFollowpos

### Funcion para determinar los simbolos de la expresion para el AFD
def simbolosAFDDirecta(correspondencias):
    simbolos = []
    ### Obtenemos todos los simbolos
    for simbolo in correspondencias:
        simbolos.append(simbolo[0])

    ### Limpiar la tabla para crear conjuntos sin elementos repetidos y quitar el simbolo #
    simbolos = list(dict.fromkeys(simbolos))
    simbolos.remove('#')

    return simbolos

### Funciones para el proceso de obtener Dstates y Dtrans
### Funcion para determinar si al menos un estado de Dstates NO ESTA MARCADO
def there_is_unmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return True
    return False

### Funcion para devolver el primer estado NO MARCADO de Dstates
def return_first_unmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return i
    return False

### Funcion para devolver los conjuntos de estadoos de la estructura Dstates
def return_states_D(Dstates):
    estados = []
    for estado in Dstates:
        estados.append(estado[0])

    return estados

### Funcion para determinar si un estado esta dentro de Dstates (a forma de conjuntos)
def state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate):
            keep = True
            for elemento in estado:
                if elemento not in Dstate:
                    keep = False
                    break
            if keep:
                return True
    return False

### Funcion para devolver un estado que este en Dstates (a forma de conjuntos)
def return_state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate[0]):
            keep = True
            for elemento in estado:
                if elemento not in Dstate[0]:
                    keep = False
                    break
            if keep:
                return Dstate
    return False

### Funcion para determinar la correspondencias a forma de posiciones
def buscar_correspondencia(S, simbolo, correspondencias):
    busqueda = []

    ### Se hace una busqueda segun la posicion en S[0]
    for posicion in S[0]:
        for correspondencia in correspondencias:
            if (correspondencia[1] == posicion) and (correspondencia[0] == simbolo):
                busqueda.append(posicion)

    return busqueda

### Funcion para hacer la traduccion de Nodos a un AFD con el nodo raiz, los simbolos de la expresion, la tabla de followpos y las correspondencias
def traduccionAFDDirecta(nodoRoot, simbolos, followpos, correspondencias):
    Dstates = []
    Dtran = []
    contador = 0
    ### Unmarked = 0 | Marked = 1
    ### Estructura [EstadosAFN, Mark, EstadoAFD]
    Dstates.append([nodoRoot.firstpos, 0, contador])
    while there_is_unmarked(Dstates):
        ### Marcar un estado S
        estadoS = return_first_unmarked(Dstates)
        estadoS[1] = 1
        ### Ciclo para cada simbolo del Nodo
        if 'ε' in simbolos:
            simbolos.remove('ε')
        for simbolo in simbolos:
            ### Busco los valores dentro de S que correspondan a 
            posiciones = buscar_correspondencia(estadoS, simbolo, correspondencias)
            ### Calcular followpos de todas las posiciones y Unirlos
            U = []
            for posicion in posiciones:
                U = U + copy.deepcopy(followpos[posicion])
            U = list(dict.fromkeys(U))

            ### Obtener los estados de U
            DOnlyStates = return_states_D(Dstates)
            nuevoEstado = []
            if U:
                if not state_in_states(U, DOnlyStates):
                    contador = contador + 1
                    nuevoEstado = [U, 0, contador]
                    Dstates.append([U, 0, contador])
                else:
                    nuevoEstado = return_state_in_states(U, Dstates)

                ### Agregar U a Dtran como una lista [estadoAFD, simboloTransicion, estadoAFD]
                Dtran.append([estadoS[2], simbolo, nuevoEstado[2]])

    return Dstates, Dtran

### Funcion que permite generar un AFD en forma de Nodo a partir de Dstates, Dtran, simbolos de la expresion y la posicion de #
def convertirAFDDirectaNodo(Dstates, Dtran, simbolos, posicionesFinales):
    nodo = Nodo('')

    nodo.posicionesFinalesAFD1 = posicionesFinales
    nodo.dStatesAFD1 = Dstates

    ### Agregar simbolos de AFD
    simbol = copy.deepcopy(simbolos)
    if 'ε' in simbol:
        simbol.remove('ε')
    nodo.simbolos = simbol

    ### Agregar estados de AFD Directa
    for estado in Dstates:
        nodo.estados.append(estado[2])
    
    ### Agregar estado inicial de AFD Directa
    nodo.estadoInicial.append(Dstates[0][2])

    ### Agregar estados finales de AFD Directa
    for estado in Dstates:
        for posicionFinal in posicionesFinales:
            if posicionFinal in estado[0]:
                nodo.estadosFinales.append(estado[2])

    ### Agregar transiciones de AFD
    nodo.transiciones = copy.deepcopy(Dtran)

    return nodo
