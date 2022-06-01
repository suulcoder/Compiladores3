### Disenio de Lenguajes de Programacion
### Saul Contreras

import math

### Definir los operadores
def is_op(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False
    
### Funcion para poder determinar si hay al menos un par de nodos que se este concatenando 
def there_is_concat(expresion):
    concatenacion = False
    for x in range(len(expresion) -1 ):
        if not is_op(expresion[x]):
            if not is_op(expresion[x + 1]):
                concatenacion = True
                break

    return concatenacion

### Funcion para poder agrupar en una lista un par de nodos que se esten concatenando
def group_concat(expresion):
    separacion = []
    saltar = False
    for i in range(len(expresion)):  
        if saltar == False:  
            if i != (len(expresion) - 1):
                if (not is_op(expresion[i])) and (not is_op(expresion[i + 1])):
                    separacion.append([expresion[i], expresion[i + 1]])
                    saltar = True
                else:
                    separacion.append(expresion[i])
            else:
                separacion.append(expresion[i])
                return separacion
        else:
            if i != (len(expresion) - 1): 
                separacion.append(expresion[i + 1])
            else:
                return separacion
    return separacion

### Funcion para convertir una expresion "string" a una estructura de arbol hecha a partir de listas
def conversionExpresionRegular(expresionString):
    pasar = True
    mensaje = ''
    expresionString = expresionString.replace(' ', '')

    ### Se determina si hay errores en la expresion
    if '||' in expresionString:
        mensaje = 'No puede tener 2 "|" juntos en la expresion'
        pasar = False
        return [], pasar, mensaje

    if ('(|' in expresionString) or ('(*' in expresionString) or ('(?' in expresionString) or ('(+' in expresionString):
        mensaje = 'Un operador no puede estar despues de un parentesis en la expresion'
        pasar = False
        return [], pasar, mensaje
    
    if is_op(expresionString[0]):
        mensaje = 'No puede tener un operador al principio de la expresion'
        pasar = False
        return [], pasar, mensaje

    if expresionString[-1] == '|':
        mensaje = 'No puede tener el operador "|" al final de la expresion'
        pasar = False
        return [], pasar, mensaje

    if '|)' in expresionString:
        mensaje = 'No puede tener el operador "|" antes del cierre de parentesis en la expresion'
        pasar = False
        return [], pasar, mensaje

    ### Pasamos la expresion a una lista
    expresion = []
    for caracterExpresion in expresionString:
        expresion.append(caracterExpresion)

    ### Encerramos la expresion entre parentesis
    expresion = ["("] + expresion + [")"]
    cantidadParentesis = 0
    guardarIzq = []
    guardarDer = []

    ### Se determina cual es el parentesis mas interno para empezar a definir las precedencias dentro de este
    while ("(" in expresion) or (")" in expresion):
        while "(" in expresion:
            cantidadParentesis = cantidadParentesis + 1
            indice = expresion.index('(')
            guardarIzq = guardarIzq + expresion[:indice+1]
            expresion = expresion[indice+1:]

        while ")" in expresion:
            if cantidadParentesis > 0:
                cantidadParentesis = cantidadParentesis - 1
                indice = expresion.index(')')
                guardarDer = expresion[indice:] + guardarDer
                expresion = expresion[:indice]
            else:
                mensaje = 'Parentesis colocados incorrectamente en la expresion'
                pasar = False
                return [], pasar, mensaje

        ### Comenzamos a definir las precedencias
        ### Primero va *, + o ?
        while ('+' in expresion) or ('?' in expresion) or ('*' in expresion):
            ### Determinar que operacion hacer primero dada la precedencia en posicion
            mas = []
            asterisco = []
            interrogacion = []

            orden = []
            primero = None
            indi = math.inf

            ### Se obtiene la posicion de cada simbolo
            if '+' in expresion:
                mas = ['+', expresion.index('+')]
            if '*' in expresion:
                asterisco = ['*', expresion.index('*')]
            if '?' in expresion:
                interrogacion = ['?', expresion.index('?')]

            ### Se agregan a una lista a ordenar los que aparezcan
            if mas:
                orden.append(mas)
            if asterisco:
                orden.append(asterisco)
            if interrogacion:
                orden.append(interrogacion)

            ### Se define cual aparece primero
            for i in orden:
                if i[1] < indi:
                    indi = i[1]
                    primero = i[0]

            ### Agrupamos en una lista el operador con su nodo
            index = expresion.index(primero)
            try:
                caracterSeparacion = expresion.pop(index-1)
                operador = expresion.pop(index-1)

                sep1 = expresion[:index-1]
                sep2 = expresion[index-1:]

                if not sep1:
                    sep1 = [caracterSeparacion, operador]
                    expresion = [sep1] + sep2
                else:
                    sep1.append([caracterSeparacion, operador])
                    expresion = sep1 + sep2
            except IndexError:
                mensaje = 'Error en expresion'
                pasar = False
                return [], pasar, mensaje

        ### Luego va la concatenacion
        while there_is_concat(expresion):
            ### Se realiza el agrupamiento el primer par de nodos a concatenar
            expresion = group_concat(expresion)

        ### De ultimo va el OR
        while '|' in expresion:
            ### Agrupamos en una lista el operador con su nodo izquierdo y su nodo derecho
            index = expresion.index('|')
            try:
                caracterSeparacion = expresion.pop(index-1)
                operador = expresion.pop(index-1)
                caracterSeparacion2 = expresion.pop(index-1)

                sep1 = expresion[:index-1]
                sep2 = expresion[index-1:]

                if not sep1:
                    sep1 = [caracterSeparacion, operador, caracterSeparacion2]
                    expresion = [sep1] + sep2
                else:
                    sep1.append([caracterSeparacion, operador, caracterSeparacion2])
                    expresion = sep1 + sep2
            except IndexError:
                mensaje = 'Error en expresion'
                pasar = False
                return [], pasar, mensaje

        ### Volvemos a ajustar la expresion completa quitando los parentesis y volviendo a procesar la lista
        if ("(" in guardarIzq) and (")" in guardarDer):
            if "(" in guardarIzq:
                guardarIzq.pop(-1)
            if ")" in guardarDer:
                guardarDer.pop(0)
            expresion = guardarIzq + [expresion] + guardarDer
            guardarIzq = []
            guardarDer = []
        else:
            mensaje = 'Parentesis colocados incorrectamente en la expresion'
            pasar = False
            return [], pasar, mensaje

    ### Devolvemos la expresion procesada a la estructura de listas, la bandera que indica si hay o no error en la expresion, y el mensaje de error si es que exite
    return expresion, pasar, mensaje

