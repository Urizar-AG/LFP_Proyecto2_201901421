reservadas = ['Claves', 'Registros', 'imprimir', 'imprimirln', 'conteo', 'promedio',
              'contarsi', 'datos', 'sumar', 'max', 'min', 'exportarReporte']

listado = [] #Listado de Lexemas reconocidos en la lectura.
tokens = [] #Listado de Tokens
errores = [] #Listado de Errores


#Convierte a ascii y verifica si corresponde a algún caracter.
def isLetra(c):
    if ((ord(c)>=65 and ord(c)<=90) or (ord(c)>=97 and ord(c)<=122)
        or (ord(c)>=128 and ord(c)<=154) or (ord(c)>=160 and ord(c)<=165)
        or (ord(c)>=181 and ord(c)<=183) or (ord(c)==198 or ord(c)==199)
        or (ord(c)>=210 and ord(c)<=216) or (ord(c)>=224 and ord(c)<=237)):
        return True
    else:
        return False

def isNumero(c):
    if(ord(c)>=48 and ord(c)<=57):
        return True
    else:
        return False
    
def isSimbolo(c):
    if(ord(c)==40 or ord(c)==41 or ord(c)==44 or ord(c)==59 or ord(c)==61 
        or ord(c)==91 or ord(c)==93 or ord(c)==123 or ord(c)==125):
        return True
    else:
        return False

def automata(doc):

    datos = doc + '~'
    estado = 0
    lex = ''
    fila = 1
    columna = 0
    for c in datos:
        if estado == 0:
            if isLetra(c):
                lex += c
                estado = 1
            elif ord(c) == 43 or ord(c) == 45:
                #43 -> +  | 45 -> -
                lex += c
                estado = 2
            elif isNumero(c):
                lex += c
                estado = 3
            elif ord(c) == 34:
                #34 -> "
                lex += c
                estado = 4
            elif isSimbolo(c):
                lex += c
                estado = 5
            elif ord(c) == 35:
                #35 -> #
                lex += c
                estado = 6
            elif ord(c) == 39:
                #39 -> '
                lex += c
                estado = 7
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    #errores = [lexema encontrado, caracter esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                lex = ''
                estado = 0
        elif estado == 1:
            if isLetra(c):
                lex += c
                estado = 1
            elif isNumero(c):
                lex += c
                estado = 1
            elif ord(c) == 95:
                #95 -> _
                lex += c
                estado = 1
            else:
                #Aceptación
                #aux = [lexema, fila, columna]
                aux = [lex, fila, columna - (len(lex) - 1)]
                listado.append(aux)
                lex = ''
                estado = 0
                #Redirección
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                elif isLetra(c):
                    lex += c
                    estado = 1
                elif ord(c) == 43 or ord(c) == 45:
                    lex += c
                    estado = 2
                elif isNumero(c):
                    lex += c
                    estado = 3
                elif ord(c) == 34:
                    lex += c
                    estado = 4
                elif isSimbolo(c):
                    lex += c
                    estado = 5
                elif ord(c) == 35:
                    lex += c
                    estado = 6
                elif ord(c) == 39:
                    lex += c
                    estado = 7
                else:
                   #errores = [lexema, caracter esperado, fila, columna]
                    aux = [c, 'Caracter Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
        elif estado == 2:
            if isNumero(c):
                lex += c
                estado = 3
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    #errores = [token encontrado, token esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                lex = ''
                estado = 0
        elif estado == 3:
            if isNumero(c):
                lex += c
                estado = 3
            elif ord(c) == 46:
                lex += c
                estado = 8
            else:
                #Aceptación
                #aux = [lexema, fila, columna]
                aux = [lex, fila, columna - (len(lex) - 1)]
                listado.append(aux)
                lex = ''
                estado = 0
                #Redirección
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                elif isLetra(c):
                    lex += c
                    estado = 1
                elif ord(c) == 43 or ord(c) == 45:
                    lex += c
                    estado = 2
                elif isNumero(c):
                    lex += c
                    estado = 3
                elif ord(c) == 34:
                    lex += c
                    estado = 4
                elif isSimbolo(c):
                    lex += c
                    estado = 5
                elif ord(c) == 35:
                    lex += c
                    estado = 6
                elif ord(c) == 39:
                    lex += c
                    estado = 7
                else:
                    #errores = [token encontrado, token esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
        elif estado == 4:
            if ord(c) == 34:
                lex += c
                estado = 5
            else:
                lex += c
                estado = 4
        elif estado == 5:
            #Aceptación
            #aux = [lexema, fila, columna]
            aux = [lex, fila, columna - (len(lex) - 1)]
            listado.append(aux)
            lex = ''
            estado = 0
            #Redirección
            if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                pass
            elif isLetra(c):
                lex += c
                estado = 1
            elif ord(c) == 43 or ord(c) == 45:
                lex += c
                estado = 2
            elif isNumero(c):
                lex += c
                estado = 3
            elif ord(c) == 34:
                lex += c
                estado = 4
            elif isSimbolo(c):
                lex += c
                estado = 5
            elif ord(c) == 35:
                lex += c
                estado = 6
            elif ord(c) == 39:
                lex += c
                estado = 7
            else:
                #errores = [token encontrado, token esperado, fila, columna]
                aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                errores.append(aux)
        elif estado == 6:
            if ord(c) != 10:
                lex += c
                estado = 6
            else:
                #Aceptación
                #aux = [lexema, fila, columna]
                aux = [lex, fila, columna - (len(lex) - 1)]
                listado.append(aux)
                lex = ''
                estado = 0
                #Redirección
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                elif isLetra(c):
                    lex += c
                    estado = 1
                elif ord(c) == 43 or ord(c) == 45:
                    lex += c
                    estado = 2
                elif isNumero(c):
                    lex += c
                    estado = 3
                elif ord(c) == 34:
                    lex += c
                    estado = 4
                elif isSimbolo(c):
                    lex += c
                    estado = 5
                elif ord(c) == 35:
                    lex += c
                    estado = 6
                elif ord(c) == 39:
                    lex += c
                    estado = 7
                else:
                    #errores = [token encontrado, token esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
        elif estado == 7:
            if ord(c) == 39:
                lex += c 
                estado = 9
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    #errores = [token encontrado, token esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                lex = ''
                estado = 0
        elif estado == 8:
            if isNumero(c):
                lex += c
                estado = 8
            else:
                #Aceptación
                aux = [lex, fila, columna - (len(lex) - 1)]
                listado.append(aux)
                lex = ''
                estado = 0
                #Redirección
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                elif isLetra(c):
                    lex += c
                    estado = 1
                elif ord(c) == 43 or ord(c) == 45:
                    lex += c
                    estado = 2
                elif isNumero(c):
                    lex += c
                    estado = 3
                elif ord(c) == 34:
                    lex += c
                    estado = 4
                elif isSimbolo(c):
                    lex += c
                    estado = 5
                elif ord(c) == 35:
                    lex += c
                    estado = 6
                elif ord(c) == 39:
                    lex += c
                    estado = 7
                else:
                    #errores = [token encontrado, token esperado, fila, columna]
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
        elif estado == 9:
            if ord(c) == 39:
                lex += c
                estado = 10
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                    lex = ''
                    estado = 0
        elif estado == 10:
            if ord(c) == 39:
                lex += c
                estado = 11
            else:
                lex += c
                estado = 10
        elif estado == 11:
            if ord(c) == 39:
                lex += c
                estado = 12
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                lex = ''
                estado = 0
        elif estado == 12:
            if ord(c) == 39:
                lex += c
                estado = 5
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    aux = [c, 'Caracteres Inesperado', 'Lexico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
                lex = ''
                estado = 0
        
        # Control de filas y columnas
        # Salto de Linea
        if (ord(c) == 10):
            columna = 0
            fila += 1
            continue
        # Tab Horizontal
        elif (ord(c) == 9):
            columna += 4
            continue
        # Espacio
        elif (ord(c) == 32):
            columna += 1
            continue
        
        columna += 1
        