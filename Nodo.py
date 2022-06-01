### Disenio de Lenguajes de Programacion
### Saul Contreras
import copy

### Definicion de la clase Nodo
class Nodo:
    def __init__(self, expresion):
        ### Se guardan los datos que posee un automata
        self.exp = expresion
        self.tipoCaracter = ''
        self.estados = [] # Conjunto de estados
        self.simbolos = [] # Conjunto de simbolos
        self.estadoInicial = [] # Estado inicial
        self.estadosFinales = [] # Conjunto de estados finales
        self.transiciones = [] # Transiciones
                
        ### Datos a almacenar para la construccion de un AFD Directa
        self.hijos = []
        self.posicion = None
        self.nullable = None
        self.firstpos = []
        self.lastpos = []
        self.tipoNodo = None

        self.dStatesAFD1 = None
        self.posicionesFinalesAFD1 = None

    ### Funcion para crear los nodos hojas de una expresion
    def transicionBase(self, correlativoEstado):
        estadoFinal = correlativoEstado + 1

        self.simbolos = [self.exp]
        self.estadoInicial = [correlativoEstado]
        self.estadosFinales = [estadoFinal]
        self.estados = [correlativoEstado, estadoFinal]
        self.transiciones = [[
            correlativoEstado, # Estado inicial
            self.exp, # Transicion
            estadoFinal # Estado final
        ]]

        return estadoFinal + 1

    ### Funcion para poder guardar la informacion de los nodos en la construccion de un AFD Directa
    def operacionesBase(self, correlativoPosicion):
        ### Como es un Nodo base entonces no tiene hijos
        self.hijos = []

        ### Le damos una posicion a la hoja si el simbolo es diferente a ε
        if self.exp == 'ε':
            self.posicion = None
            correlativoPosicion = correlativoPosicion - 1
        else:
            self.posicion = correlativoPosicion

        ### Un nodo caracter solo es nullable cuando es ε
        if self.exp == 'ε':
            self.nullable = True
        else:
            self.nullable = False

        ### Un nodo caracter solo tiene firstpos cuando no es ε
        if self.exp == 'ε':
            self.firstpos = []
        else:
            self.firstpos = [self.posicion]

        ### Un nodo caracter solo tiene lastpos cuando no es ε
        if self.exp == 'ε':
            self.lastpos = []
        else:
            self.lastpos = [self.posicion]

        return correlativoPosicion + 1

    ### Vamos a hacer la definicion para Nodos mas complejos de un AFN
    ### OR
    def transicionOrAFN(self, nodo1, nodo2, correlativo):
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo1.simbolos + nodo2.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo+1]

        self.estados = nodo1.estados + nodo2.estados + [correlativo,correlativo+1]
        self.estados = list(dict.fromkeys(self.estados))

        self.transiciones = nodo1.transiciones + nodo2.transiciones + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodo1.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodo2.estadoInicial[0]
        ]] + [[
            nodo1.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]] + [[
            nodo2.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    ### CONCAT
    def transicionConcatAFN(self, nodo1, nodo2, correlativo):
        self.simbolos = nodo1.simbolos + nodo2.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = nodo1.estadoInicial
        self.estadosFinales = nodo2.estadosFinales

        self.estados = nodo1.estados + nodo2.estados
        self.estados = list(dict.fromkeys(self.estados))
        self.estados.remove(nodo1.estadosFinales[0])

        self.transiciones = nodo1.transiciones + nodo2.transiciones

        for i in self.transiciones:
            if i[2] == nodo1.estadosFinales[0]:
                i[2] = nodo2.estadoInicial[0]

        return correlativo

    ### CERRADURA
    def transicionCerraduraAFN(self, nodo, correlativo):
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo + 1]
        self.estados = nodo.estados + [correlativo,correlativo+1]
        self.transiciones = nodo.transiciones + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodo.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', # Transicion
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    ### CERRADURA POSITIVA
    def transicionCerraduraPositivaAFN(self, nodo, correlativo):
        ### Procesamos como si fuera cerradura normal
        estadoFinal = correlativo + 1

        ### Creamos un nodo copia del original
        nodoCopia = Nodo('')
        nodoCopia.exp = nodo.exp
        nodoCopia.simbolos = copy.deepcopy(nodo.simbolos)
        nodoCopia.estados = copy.deepcopy(nodo.estados)
        nodoCopia.estadoInicial = copy.deepcopy(nodo.estadoInicial)
        nodoCopia.estadosFinales = copy.deepcopy(nodo.estadosFinales)
        nodoCopia.transiciones = copy.deepcopy(nodo.transiciones)

        self.simbolos = ['ε'] + nodo.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo + 1]
        self.estados = nodo.estados + [correlativo,correlativo+1]
        self.transiciones = nodo.transiciones + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodo.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', # Transicion
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]]

        ### Ahora le concatenamos el nodo mismo
        ### Hay que simular el nodo con el correlativo de estados en variable nodo
        ### Cambiar los estados del nodo copiado
        cantidadExtra = len(nodo.estados)

        arregloX = []
        arregloY = []

        ### Guardar relacion de estados antiguos con los nuevos
        ### Y asignacion de nuevos estados
        for i in range(cantidadExtra):
            arregloX.append(nodoCopia.estados[i])
            arregloY.append(estadoFinal + 1 + i)
            nodoCopia.estados[i] = estadoFinal + 1 + i

        ### Set de las transiciones
        for j in range(len(nodo.transiciones)):
            s = arregloX.index(nodo.transiciones[j][0])
            nodo.transiciones[j][0] = arregloY[s]

            s = arregloX.index(nodo.transiciones[j][2])
            nodo.transiciones[j][2] = arregloY[s]

        ### Set estado Inicial
        s = arregloX.index(nodoCopia.estadoInicial[0])
        nodoCopia.estadoInicial[0] = arregloY[s]

        ### Set estado Final
        s = arregloX.index(nodoCopia.estadosFinales[0])
        nodoCopia.estadosFinales[0] = arregloY[s]

        ### Concatenacion
        self.simbolos = self.simbolos + nodoCopia.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = self.estadoInicial
        nodoFinal = self.estadosFinales[0]
        self.estadosFinales = nodoCopia.estadosFinales

        self.estados = self.estados + nodoCopia.estados
        self.estados = list(dict.fromkeys(self.estados))
        self.estados.remove(nodoFinal)

        self.transiciones = self.transiciones + nodoCopia.transiciones

        for i in self.transiciones:
            if i[2] == nodoFinal:
                i[2] = nodoCopia.estadoInicial[0]

        return estadoFinal + 1 + cantidadExtra

    ### CERRADURA ?
    def transicionCerraduraInterogationAFN(self, nodo, correlativo):
        ### Crear el nodo Epsilon
        nodoEpsilon = Nodo('ε')
        correlativo = nodoEpsilon.transicionBase(correlativo)
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo.simbolos + nodoEpsilon.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))


        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo+1]

        self.estados = nodo.estados + nodoEpsilon.estados + [correlativo,correlativo+1]
        self.estados = list(dict.fromkeys(self.estados))

        self.transiciones = nodo.transiciones + nodoEpsilon.transiciones + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', # Transicion
            nodoEpsilon.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]] + [[
            nodoEpsilon.estadosFinales[0],
            'ε', # Transicion
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    ### CERRADURA EPSILON (Para usar en la simulacion de automatas)
    ### Funcion que nos permite determinar a que estados podemos llegar a traves de transiciones Epsilon desde un conjunto de "estados"
    ### El parametro "estados" puede ser uno o varios estados
    def cerraduraE(self, estados):
        estados = copy.deepcopy(estados)
        conjuntoS = []
        for i in estados:
            conjuntoS.append(i)
            siguienteEstado = i
            movimientosE = []
            for j in self.transiciones:
                if j[0] == siguienteEstado and j[1] == 'ε':
                    movimientosE.append(copy.deepcopy(j))
            
            while movimientosE:
                siguienteTransicion = movimientosE.pop()
                if siguienteTransicion[1] == 'ε':
                    conjuntoS.append(siguienteTransicion[2])
                    for k in self.transiciones:
                        if k[0] == siguienteTransicion[2] and (k[0] not in conjuntoS or k[2] not in conjuntoS):
                            movimientosE.append(k)
                
        conjuntoS = list(dict.fromkeys(conjuntoS))
        return conjuntoS

    ### MOVE (Para usar en la simulacion de automatas)
    ### Funcion que nos indica a que estados podemos llegar a traves de la transicion dada por el caracter "c" desde los estados "S"
    def move(self, S, c):
        conjuntoM = []
        for estado in S:
            for j in self.transiciones:
                if j[0] == estado and j[1] == c:
                    conjuntoM.append(j[2])

        return conjuntoM

    ### Vamos a hacer la definicion para Nodos operandos para la construccion de AFD Directa
    ### OR
    def transicionOrAFD(self, nodo1, nodo2):
        ### Nullable
        if nodo1.nullable or nodo2.nullable:
            self.nullable = True
        else:
            self.nullable = False

        ### Firstpos
        self.firstpos = list(dict.fromkeys(nodo1.firstpos + nodo2.firstpos))

        ### Lastpos
        self.lastpos = list(dict.fromkeys(nodo1.lastpos + nodo2.lastpos))

        ### Indicar que el nodo es de tipo OR
        self.tipoNodo = '|'
        
    ### CONCAT
    def transicionConcatAFD(self, nodo1, nodo2):
        ### Nullable
        if nodo1.nullable and nodo2.nullable:
            self.nullable = True
        else:
            self.nullable = False

        ### Firstpos
        if nodo1.nullable:
            self.firstpos = list(dict.fromkeys(nodo1.firstpos + nodo2.firstpos))
        else:
            self.firstpos = nodo1.firstpos

        ### Lastpos
        if nodo2.nullable:
            self.lastpos = list(dict.fromkeys(nodo1.lastpos + nodo2.lastpos))
        else:
            self.lastpos = nodo2.lastpos
        
        ### Indicar que el nodo es de tipo OR
        self.tipoNodo = '.'

        ### Hijos
        self.hijos = [nodo1, nodo2]

    ### CERRADURA
    def transicionCerraduraAFD(self, nodo):
        ### Nullable
        self.nullable = True

        ### Firstpos
        self.firstpos = nodo.firstpos

        ### Lastpos
        self.lastpos = nodo.lastpos

        ### Indicar que el nodo es de tipo OR
        self.tipoNodo = '*'