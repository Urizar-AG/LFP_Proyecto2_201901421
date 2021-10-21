from reportes import reporteT, reporteE

reservadas = ['Claves', 'Registros', 'imprimir', 'imprimirln', 'conteo', 'promedio',
              'contarsi', 'datos', 'sumar', 'max', 'min', 'exportarReporte']

listado = [] #Listado de Lexemas reconocidos en la lectura.
tokens = [] #Listado de Tokens
errores = [] #Listado de Errores
pila = []#Pila para manejar los tokens en el parser.
listadoClaves = []  #Guarda las claves al reconocerlas en el parser.

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

def isReservada(palabra):
    for elemento in reservadas:
        if palabra == elemento:
            return 1
        elif palabra.lower() == elemento:
            return 2
    return 0

def quitarComillas(cadena):
    nuevaCadena = ''
    for c in cadena:
        if c != '"':
            nuevaCadena += c
    return nuevaCadena

def automata(doc):
    global listado
    global tokens
    global errores
    listado = []
    tokens = []
    errores = []

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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracter Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
                    errores.append(aux)
        elif estado == 9:
            if ord(c) == 39:
                lex += c
                estado = 10
            else:
                if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c == '~':
                    pass
                else:
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
                    aux = [c, 'Caracteres Inesperado', 'Léxico', fila, columna - (len(lex) - 1)]
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
    tokenizar()
    if len(tokens) > 0 and len(errores) == 0:
        return True
    else:
        return False

#Identifica los token y busca errores
def tokenizar():
    for elemento in listado:
        #Reservada correcta
        if isReservada(elemento[0]) == 1:
            #item = [elemento[0], tipo de token, fila, columna]
            item = [elemento[0], 'Palabra Reservada', str(elemento[1]), str(elemento[2])]
            tokens.append(item)
        #Reservada pero lexicamente mal
        elif isReservada(elemento[0]) == 2:
            item = [elemento[0], 'Identificador', str(elemento[1]), str(elemento[2])]
            tokens.append(item)       
            #errores = [lexema encontrado, caracter esperado, fila, columna]
            aux = [elemento[0], 'Se esperaba una palabra reservada', 'Léxico', elemento[1], elemento[2]]
            errores.append(aux)
        else:
            for c in elemento[0]:
                #Comilla -> Cadena
                if ord(c) == 34:
                    item = [elemento[0], 'Cadena', str(elemento[1]), str(elemento[2])]
                    tokens.append(item)
                    break
                #Número con signo
                elif ord(c) == 43 or ord(c) == 45:
                    lexema = elemento[0]
                    if len(lexema) >= 3:
                        decimal = False
                        #Signo negativo
                        if ord(c) == 45:
                            for i in range(len(lexema)):
                                #Encontro decimal
                                if ord(lexema[i]) == 46:
                                    decimal = True
                                    try:
                                        if isNumero(lexema[i-1]) and isNumero(lexema[i+1]):
                                            item = [elemento[0], 'Número Decimal', str(elemento[1]), str(elemento[2])]
                                            tokens.append(item)  
                                            break
                                        else:
                                            aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                            errores.append(aux)
                                            break
                                    except:
                                        aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                        errores.append(aux)
                                        break
                        #Signo Positivo
                        elif ord(c) == 43:
                            numero = ''
                            for i in range(len(lexema)):
                                if ord(lexema[i]) == 46:
                                    decimal = True
                                    try:
                                        if isNumero(lexema[i-1]) and isNumero(lexema[i+1]):
                                            for caracter in lexema:
                                                if ord(caracter) == 43:
                                                    pass
                                                else:
                                                    numero += caracter
                                            item = [numero, 'Número Decimal', str(elemento[1]), str(elemento[2])]
                                            tokens.append(item)  
                                            break
                                        else:
                                            aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                            errores.append(aux)
                                            break
                                    except:
                                        aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                        errores.append(aux)
                                        break
                        #Si no encontro decimal
                        if decimal == False:
                            if ord(c) == 45:
                                item = [elemento[0], 'Número Entero', str(elemento[1]), str(elemento[2])]
                                tokens.append(item)  
                                break
                            elif ord(c) == 43:
                                numero = ''
                                for character in lexema:
                                    if ord(character) != 43:
                                        numero += character
                                item = [numero,  'Número Entero', str(elemento[1]), str(elemento[2])]
                                tokens.append(item)
                                break
                    elif len(lexema) == 2:
                        if ord(c) == 45:
                            item = [elemento[0], 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break
                        elif ord(c) == 43:
                            numero = ''
                            for character in lexema:
                                if ord(character) != 43:
                                    numero += character
                            item = [numero, 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break 
                    else:
                        if ord(c) == 45:
                            item = [elemento[0], 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break
                        elif ord(c) == 43:
                            numero = ''
                            for character in lexema:
                                if ord(character) != 43:
                                    numero += character
                            item = [numero, 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break
                    break                         
                #Número sin signo
                elif isNumero(c):
                    lexema = elemento[0]
                    #Número decimal correcto se compone almenos de 3 caracteres
                    if len(lexema) >= 3:
                        decimal = False
                        for i in range(len(lexema)):
                            #Si encuentra punto
                            if ord(lexema[i]) == 46:
                                decimal = True
                                try:
                                    #Posicion anterior y siguiente sean número
                                    if isNumero(lexema[i-1]) and isNumero(lexema[i+1]):
                                        item = [elemento[0], 'Número Decimal', str(elemento[1]), str(elemento[2])]
                                        tokens.append(item)  
                                        break
                                    else:
                                        aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                        errores.append(aux)
                                        break
                                except:
                                    aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                                    errores.append(aux)
                                    break
                        if decimal == False:
                            item = [elemento[0], 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break    
                    else:
                        decimal = False
                        for c in lexema:
                            if ord(c) == 46:
                                decimal = True
                                break
                        if decimal == False:
                            item = [elemento[0], 'Número Entero', str(elemento[1]), str(elemento[2])]
                            tokens.append(item)  
                            break
                        elif decimal == True:
                            aux = [elemento[0], 'Se esperaba un número decimal', 'Léxico', elemento[1], elemento[2]]
                            errores.append(aux)
                            break   
                    break
                elif isSimbolo(c):
                    item = [elemento[0], 'Símbolo', str(elemento[1]), str(elemento[2])]
                    tokens.append(item)  
                    break  
                else:
                    if ord(c) == 39:
                        pass
                    elif ord(c) == 35:
                        pass
                    else:
                        aux = [elemento[0], 'Caracteres Inesperados', 'Léxico', elemento[1], elemento[2]]
                        errores.append(aux)                        
                break 
    parser()
    #print(tokens)
    #print('############################')
    #print(errores)

def generarReporteTokens():
    reporteT(tokens)

def generarReporteErrores():
    reporteE(errores)

def parser():
    for elemento in tokens:
        pila.append(elemento)
    validarCLAVES()
    #print(listadoClaves)


def validarCLAVES():
 
    if pila[0][1] == 'Palabra Reservada':
        if pila[0][0] == 'Claves':
            pila.pop(0)
    else:
        #errores = [lexema encontrado, caracter esperado, fila, columna]
        aux = [pila[0][0], 'Se esperaba palabra reservada', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux)
        pila.pop(0)
    validarSimboloIgual('RClaves')

def validarSimboloIgual(parametro):
    if pila[0][0] == '=':
        pila.pop(0)
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo =', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux)        
        pila.pop(0)
    validarCorchete(parametro, 'a')

def validarCorchete(parametro, modo):
    if parametro == 'RClaves':
        if modo == 'a':
            if pila[0][0] == '[':
                pila.pop(0)
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo [', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux)        
                pila.pop(0)

            validarLClaves()
        elif modo == 'c':
            if pila[0][0] == ']':
                return True
            else:
                #aux = [pila[0][0], 'Se esperaba el símbolo ]', 'Sintáctico', pila[0][2], pila[0][3]]
                #errores.append(aux)        
                #pila.pop(0)
                return False

def validarLClaves():
    if pila[0][1] == "Cadena":
        listadoClaves.append(quitarComillas(pila[0][0]))
        pila.pop(0)
    else:
        aux = [pila[0][0], 'Se esperaba una clave', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux)        
        pila.pop(0) 
    validarLClaveP()

def validarLClaveP():
    if pila[0][0] == ',':
        pila.pop(0)
        res0 =  validarTkCadena()
        if res0 == True:
            pila.pop(0)
            validarLClaveP()
        else:
            res1 = validarCorchete('RClaves', 'c')
            if res1 == True:
                aux = [pila[0][0], 'Se esperaba cadena', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux)        
                pila.pop(0)
            else:
                if pila[0][0] == ',':
                    aux = [pila[0][0], 'Se esperaba cadena', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)        
                    pila.pop(0)
                    validarLClaveP()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ,', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)        
                    pila.pop(0)
                    validarLClaveP()

    else:
        res0 = validarTkCadena()
        if res0 == True:
            aux = [pila[0][0], 'Se esperaba el símbolo ,', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)        
            pila.pop(0)
            validarLClaveP()
        else:
            res1 = validarCorchete('RClaves', 'c')
            if res1 != True:
                aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux)        
                pila.pop(0)
                validarLClaveP()
            else:
                pila.pop(0)
                
def validarTkCadena():
    if pila[0][1] == 'Cadena':
        listadoClaves.append(quitarComillas(pila[0][0]))
        #pila.pop(0)
        return True
    else:
        #aux = [pila[0][0], 'Se esperaba cadena', 'Sintáctico', pila[0][2], pila[0][3]]
        #errores.append(aux)        
        #pila.pop(0)
        return False
