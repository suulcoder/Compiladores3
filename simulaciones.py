### Disenio de Lenguajes de Programacion
### Saul Contreras

def simulacionAFN(afn, cadena):
    ### Se obtiene el conjunto de estados S a partir la cerradura E de los estados iniciales del AFN
    S = afn.cerraduraE(afn.estadoInicial)
    ### Iteramos sobre los caracteres de la cadena dada
    for c in cadena:
        ### Se obtiene el move de los estados en S con el caracter c
        ### Al resultado le aplicamos cerradura E y obtenemos el nuevo conjunto de estados S
        S = afn.cerraduraE(afn.move(S, c))

    ### Se procesa la interesccion entre la lista del conjunto de los estados S y la lista del conjunto de estados finales del AFN
    interseccion = set.intersection(set(S), set(afn.estadosFinales))
    interseccion = list(interseccion)

    ### Se determina si existe interesccion
    ### Si la hay entonces la cadena pertenece al Lenguaje representado por el AFN,
    ### Si no hay entonces la cadena no pertenece al Lenguaje representado por el AFN
    if interseccion:
        return True
    else:
        return False

### Funcion para realizar la simulacion de un AFD, dado un AFD en forma de Nodo y un a cadena de caracteres
def simulacionAFD(afd, cadena):
    ### Se obtiene el estado s siendo el estado inicial del AFD
    s = afd.estadoInicial

    ### Iteramos sobre los caracteres de la cadena dada
    for c in cadena:
        ### Se obtiene s atraves del move del estado s con el caracter c
        s = afd.move(s, c)

    ### Se procesa la interesccion entre la lista del estado s y la lista del conjunto de estados finales del AFD
    interseccion = set.intersection(set(s), set(afd.estadosFinales))
    interseccion = list(interseccion)

    ### Se determina si existe interesccion
    ### Si la hay entonces la cadena pertenece al Lenguaje representado por el AFD,
    ### Si no hay entonces la cadena no pertenece al Lenguaje representado por el AFD
    if interseccion:
        return True, interseccion
    else:
        return False, None

### Funcion para realizar la simulacion de un AFD
def simulacionAFD2(afd, cadena, posicion, tokens, ignore):
    ### Se obtiene el estado s siendo el estado inicial del AFD
    s = afd.estadoInicial

    token = ''
    transicion = True
    posicionInicial = posicion
    ultimaPosicionToken = posicion
    interseccion = None

    ### Se determina una transicion
    while transicion and (posicion < len(cadena)):
        caracter = str(ord(cadena[posicion]))

        ### Se revisa si el conjunto ignore esta definido
        if ignore:
            ### Se revisa si el caracter esta en ignore para ignorarlo
            if int(caracter) in ignore:
                posicion = posicion + 1
                continue

        ### Iteramos sobre los caracteres de la cadena dada
        for i in caracter:
            ### Se obtiene s atraves del move del estado s con el caracter c
            s = afd.move(s, i)

        if not s:
            transicion = False
            posicion = posicion + 1

        if s:
            ### Se procesa la interesccion entre la lista del estado s y la lista del conjunto de estados finales del AFD
            interseccion = set.intersection(set(s), set(afd.estadosFinales))
            interseccion = list(interseccion)

            ### Se determina si existe interesccion
            ### Si la hay entonces la cadena pertenece al Lenguaje representado por el AFD,
            ### Si no hay entonces la cadena no pertenece al Lenguaje representado por el AFD
            if interseccion:
                ultimaPosicionToken = posicion

                ### Primero se revisa a cual de los estados del automata corresponde la interseccion
                for estado in afd.dStatesAFD1:
                    if estado[2] == interseccion[0]:
                        subEstados = estado[0]
                        estadosFinales = []
                        for subEstado in subEstados:
                            if subEstado in afd.posicionesFinalesAFD1:
                                estadosFinales.append(subEstado)

                ### Ahora obtenemos el valor minimo de los estadosFinales
                minimo = min(estadosFinales)

                ### Se revisa la posicion que ocupa en el minimo en el arreglo de posicionesFinalesAFD1
                index = afd.posicionesFinalesAFD1.index(minimo)

                token = list(tokens.keys())[index]

            ### Siguiente posicion
            posicion = posicion + 1
    
    ### Se reconoce como ultima posicion al siguiente caracter y se recorta la cadena original
    ultimaPosicionToken = ultimaPosicionToken + 1
    cadenaRetornar = cadena[posicionInicial:ultimaPosicionToken]
    return token, ultimaPosicionToken, cadenaRetornar