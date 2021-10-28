from reportes import reporteT, reporteE

reservadas = ['Claves', 'Registros', 'imprimir', 'imprimirln', 'conteo', 'promedio',
              'contarsi', 'datos', 'sumar', 'max', 'min', 'exportarReporte']

listado = [] #Listado de Lexemas reconocidos en la lectura.
tokens = [] #Listado de Tokens
errores = [] #Listado de Errores
pila = []#Pila para manejar los tokens en el parser.
listadoClaves = []  #Guarda las claves al reconocerlas en el parser.
listadoRegistros = [] #Guarda los registros al reconocerlas en el parser.
registrar = [] #Lista que almacena temporalmente un conjunto de registor {}
listadoReporteria = []#Almacena el listado de reportes a realizar.(reporte = comando del lenguaje del programa).
auxReporteria = []#Auxiliar para almacenar el reporte(reporte =  comandodel lenguaje del programa).

#----------------------------------------------------------------------------------------------------------------------------------------
def getListados():
    return listadoClaves, listadoRegistros

#Devuelve la listad de comandos a ejecutar
def getReporteria():
    return listadoReporteria

def generarReporteTokens():
    reporteT(tokens)

def generarReporteErrores():
    reporteE(errores)

#---------------------------------------------------------- Análisis léxico y sintáctico ------------------------------------------------

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

#convierte los números a int\float y quita las comillas dobles de las cadenas
def darFormato(entrada, tipo):
    if tipo == 'Cadena':
        nuevaCadena = ''
        for c in entrada:
            if c != '"':
                nuevaCadena += c
        return nuevaCadena
    elif tipo == 'Número Entero':
        return int(entrada)
    elif tipo == 'Número Decimal':
        return float(entrada)

def automata(doc):
    global listado
    global tokens
    global errores
    global pila
    global listadoClaves
    global listadoRegistros
    global registrar
    global listadoReporteria
    global auxReporteria
    #Limpiando las listas pra un nuevo scanneo
    listado = []
    tokens = []
    errores = []
    pila = []
    listadoClaves = []
    listadoRegistros = []
    registrar = []
    listadoReporteria = []
    auxReporteria = []

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

#Identifica los token y busca errores léxicos.
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
    if len(errores) == 0:
        parser()
    #print(tokens)
    #print('############################')
    #print(errores)

def parser():
    for elemento in tokens:
        pila.append(elemento)
    acep = ['~', 'Aceptacion', 'x', 'y']
    pila.append(acep)
    validarCLAVES()
    if pila[0][0] != '~' and pila[0][1] != 'Aceptacion':
        validarREGISTROS()
    if pila[0][0] != '~' and pila[0][1] != 'Aceptacion':
        validarREPORTES()
    print(errores)
    print("----------------------------------------------------------")
    print(listadoRegistros)

#Funciones pertenecientes al parser.
def validarCLAVES():
 
    if pila[0][1] == 'Palabra Reservada':
        if pila[0][0] == 'Claves':
            pila.pop(0)
    else:
        #errores = [lexema encontrado, caracter esperado, fila, columna]
        aux = [pila[0][0], 'Se esperaba palabra reservada', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux)
        pila.pop(0)
    validarSimboloIgual('RClaves', 'RClaves')

def validarSimboloIgual(parametro, parametro2):
    if parametro2 == 'RClaves':
        if pila[0][0] == '=':
            pila.pop(0)
        else:
            aux = [pila[0][0], 'Se esperaba el símbolo =', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)        
            pila.pop(0)
        validarCorchete(parametro, 'a')
    elif parametro2 == 'RRegistros':
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
    elif parametro == 'RRegistros':
        if modo == 'a':
            if pila[0][0] == '[':
                pila.pop(0)
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo [', 'Sintácticto', pila[0][2], pila[0][3]]
                errores.append(aux)
                pila.pop(0)
            validarLRegistros()
        elif modo == 'c':
            if pila[0][0] == ']':
                return True
            else:
                return False

def validarLClaves():
    if pila[0][1] == "Cadena":
        listadoClaves.append(darFormato(pila[0][0],pila[0][1]))
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
        listadoClaves.append(darFormato(pila[0][0], pila[0][1]))
        #pila.pop(0)
        return True
    else:
        #aux = [pila[0][0], 'Se esperaba cadena', 'Sintáctico', pila[0][2], pila[0][3]]
        #errores.append(aux)        
        #pila.pop(0)
        return False


def validarREGISTROS():
    if len(pila) > 0:
        if pila[0][1] == 'Palabra Reservada':
            if pila[0][0] == 'Registros':
                pila.pop(0)
        else:
            #errores = [lexema encontrado, caracter esperado, fila, columna]
            aux = [pila[0][0], 'Se esperaba palabra reservada', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)
            pila.pop(0)
        validarSimboloIgual('RRegistros', 'RRegistros')        

def validarLRegistros():
    validarRegistro()

def validarRegistro():
    res = validarSimboloLlave('a')
    if res == True:
        pila.pop(0)
        validarLERegistro()
    else:
        if pila[0][0] == '~':
            pass
        else:
            res = validarCorchete('RRegistros', 'c')
            if res == True:
                pila.pop(0)
            else:
                res1 = validarElementoRegistro()
                if res1 == True:
                    aux = [pila[0][0], 'Se esperaba el símbolo {', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)
                    registrar.append(darFormato(pila[0][0],pila[0][1]))        
                    pila.pop(0)
                    validarLERegistroP()
                else:
                    aux = [pila[0][0], 'Error', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)
                    pila.pop(0)
                    validarRegistro()

def validarSimboloLlave(modo):
    if modo == 'a':
        if pila[0][0] == '{':
            return True
        else: 
            return False
    elif modo == 'c':
        if pila[0][0] == '}':
            return True
        else:
            return False

def validarLERegistro():
    global registrar
    res = validarElementoRegistro()
    if res == True:
        registrar.append(darFormato(pila[0][0], pila[0][1]))
        pila.pop(0)
        validarLERegistroP()
    else:
        res = validarSimboloLlave('c')
        if res == True:
            pila.pop(0)
            if len(registrar) == len(listadoClaves):
                listadoRegistros.append(registrar)
            registrar = []
        else:
            if pila[0][0] == ',':
                aux = [pila[0][0], 'Se esperaba un elemento registro', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux)        
                pila.pop(0)
                validarLERegistro()
            else:    
                pass

def validarElementoRegistro():
    if pila[0][1] == 'Cadena':
        return True
    elif pila[0][1] == 'Número Entero':
        return True
    elif pila[0][1] == 'Número Decimal':
        return True
    else:
        return False

def validarLERegistroP():
    global registrar
    global listadoErrores
    if pila[0][0] == ",":
        pila.pop(0)
        res = validarElementoRegistro()
        if res == True:
            registrar.append(darFormato(pila[0][0], pila[0][1]))
            pila.pop(0)
            validarLERegistroP()
        else:
            res1 = validarSimboloLlave('c')
            if res1 == True:
                aux = [pila[0][0], 'Se esperaba un elemento registro', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux)        
                pila.pop(0)
                if len(registrar) > 0:
                    if len(registrar) == len(listadoClaves):
                        listadoRegistros.append(registrar)
                registrar = []
                validarLRegistros()
            else:
                if pila[0][0] == ',':
                    aux = [pila[0][0], 'Se esperaba un elemento registro', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)        
                    pila.pop(0)
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ,', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)        
                    pila.pop(0)
                validarLERegistroP()
    else:
        res0 = validarElementoRegistro()
        if res0 == True:
            aux = [pila[0][0], 'Se esperaba el símbolo ,', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)        
            pila.pop(0)
            validarLERegistroP()
        else:
            res1 = validarSimboloLlave('c')
            if res1 != True:
                res2 = validarSimboloLlave('a')
                if res2 == True:
                    aux = [pila[0][0], 'Se esperaba el simbolo }', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux)
                    if len(registrar) == len(listadoClaves):        
                        listadoRegistros.append(registrar)
                    registrar = []
                    validarRegistro()
                else:
                    if pila[1][0] == '~':
                        aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
                        errores.append(aux)
                        if len(registrar) == len(listadoClaves):
                            listadoRegistros.append(registrar)
                        registrar = []
                        pila.pop(0)
                    elif pila[1][1] == 'Palabra Reservada':
                        aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
                        errores.append(aux)
                        if len(registrar) == len(listadoClaves):     
                            listadoRegistros.append(registrar)
                        registrar = []   
                        pila.pop(0)
                        #validarLERegistroP()
                    elif pila[0][0] == ']':
                        aux = [pila[0][0], 'Se esperaba el símbolo }', 'Sintáctico', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        if len(registrar) == len(listadoClaves):
                            listadoRegistros.append(registrar)
                        registrar = []       
                        pila.pop(0)
                    else:
                        validarLERegistroP()                        
                        aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
                        errores.append(aux)        
                        pila.pop(0)
                        validarLERegistroP()
            else:
                pila.pop(0)
                if len(registrar) == len(listadoClaves):
                    listadoRegistros.append(registrar)
                registrar = []
                validarRegistro()

def validarParentesis(simbolo, modo):
    if modo == 'a':
        if simbolo == '(':
            return True
        else:
            return False
    elif modo == 'c':
        if simbolo == ')':
            return True
        else:
            return False

#Vacia la pila de tokens hasta encontrar un token 'Palabra Reservada'
def popPila():
    global auxReporteria
    var1 = False
    var2 = False
    for token in pila:
       
        if pila[0][0] == '~' and pila[0][1] == 'Aceptacion':
            aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)        
            auxReporteria = []
            var1 = True
            break
        elif pila[0][0] != '~' and token[1] != 'Aceptacion' and pila[0][1] != 'Palabra Reservada':
            pila.pop(0)
        elif pila[0][1] == 'Palabra Reservada':
            var2 = True
            break
    if var1 == True:
        pass
    elif var2 == True:
        validarReporte()


def validarREPORTES():
    validarReporte()

def validarReporte():
    if pila[0][0] == 'imprimir':
        auxReporteria.append('01')
        pila.pop(0)
        validarIMPRESION()
    elif pila[0][0] == 'imprimirln':
        auxReporteria.append('02')
        pila.pop(0)
        validarIMPRESIONLN()
    elif pila[0][0] == 'conteo':
        auxReporteria.append('03')
        pila.pop(0)
        validarCONTEO()
    elif pila[0][0] == 'promedio':
        auxReporteria.append('04')
        pila.pop(0)
        validarPROMEDIO()
    elif pila[0][0] == 'contarsi':
        auxReporteria.append('05')
        pila.pop(0)
        validarCONTARSI()
    elif pila[0][0] == 'datos':
        auxReporteria.append('06')
        pila.pop(0)
        validarDATOS()
    elif pila[0][0] == 'sumar': 
        auxReporteria.append('07')
        pila.pop(0)
        validarSUMAR()
    elif pila[0][0] == 'max':
        auxReporteria.append('08')
        pila.pop(0)
        validarMAX()
    elif pila[0][0] == 'min':
        auxReporteria.append('09')
        pila.pop(0)
        validarMIN()
    elif pila[0][0] == 'exportarReporte':
        pass
    else:
        if pila[0][0] != '~' and pila[0][1] != 'Aceptacion': 
            aux = [pila[0][0], 'Error inesperado', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux)        
            pila.pop(0)
            validarReporte()

def validarIMPRESION():
    global auxReporteria
    global listadoReporteria
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    listadoReporteria.append(auxReporteria)
                    auxReporteria = []
                    validarReporte()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarIMPRESIONLN():
    global auxReporteria
    global listadoReporteria
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    listadoReporteria.append(auxReporteria)
                    auxReporteria = []
                    validarReporte()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba una Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarCONTEO():
    global auxReporteria
    global listadoReporteria
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)
        res2 = validarParentesis(pila[0][0], 'c')
        if res2 == True:
            pila.pop(0)
            if pila[0][0] == ';':
                pila.pop(0)
                #numRegColumnas = len(listadoRegistros[0])#La cantidad de registros que tiene una fila
                numRegFilas = len(listadoRegistros)#La cantidad de filas que hay
                #total = numRegColumnas * numRegFilas
                auxReporteria.append(str(numRegFilas))
                listadoReporteria.append(auxReporteria)
                auxReporteria = []
                validarReporte()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarPROMEDIO():
    global auxReporteria
    global listadoReporteria
    campo = ''
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            #auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            campo = pila[0][0]
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    res3 = buscarClave(darFormato(campo, 'Cadena'))#Obtiene la clave a la que se le va a sacar promedio.
                    if res3[0] == True:
                        res4 = calcularPromedio(res3[1])
                        if res4 != None:
                            auxReporteria.append(res4)
                            listadoReporteria.append(auxReporteria)
                            auxReporteria = []
                            validarReporte()
                        else:
                            #Si entra aquí encontro un valor tipo string(no se puede calcular el promedio)
                            aux = [pila[0][0], 'Se esperaba un valor númerico.', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()
                    else:
                        aux = [str(campo), 'No se encontro el campo indicado.', 'Ejecución', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        auxReporteria = []
                        popPila()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarCONTARSI():
    global auxReporteria
    global listadoReporteria
    campo = ''
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            campo = darFormato(pila[0][0], 'Cadena')
            res2 = buscarClave(campo)
            if res2[0] == True:
                pila.pop(0)
                if pila[0][0] == ',':
                    pila.pop(0)
                    if pila[0][1] == 'Cadena':
                        valor = darFormato(pila[0][0], 'Cadena')
                        pila.pop(0)                
                        res3 = validarParentesis(pila[0][0], 'c')
                        if res3 == True:
                            pila.pop(0)
                            if pila[0][0] == ';':
                                pila.pop(0)
                                res4 = calcularContarsi(res2[1], valor)
                                auxReporteria.append(res4)
                                listadoReporteria.append(auxReporteria)
                                auxReporteria = []
                                validarReporte()
                            else:
                                aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                                errores.append(aux) 
                                auxReporteria = []
                                popPila()  
                        else:
                            aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()                              
                    elif pila[0][1] == 'Número Entero':
                        valor = darFormato(pila[0][0], 'Número Entero')
                        pila.pop(0)                
                        res3 = validarParentesis(pila[0][0], 'c')
                        if res3 == True:
                            pila.pop(0)
                            if pila[0][0] == ';':
                                pila.pop(0)
                                res4 = calcularContarsi(res2[1], valor)
                                auxReporteria.append(res4)
                                listadoReporteria.append(auxReporteria)
                                auxReporteria = []
                                validarReporte()
                            else:
                                aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                                errores.append(aux) 
                                auxReporteria = []
                                popPila()  
                        else:
                            aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()                      
                    elif pila[0][1] == 'Número Decimal':
                        valor = darFormato(pila[0][0], 'Número Decimal')
                        pila.pop(0)                
                        res3 = validarParentesis(pila[0][0], 'c')
                        if res3 == True:
                            pila.pop(0)
                            if pila[0][0] == ';':
                                pila.pop(0)
                                res4 = calcularContarsi(res2[1], valor)
                                auxReporteria.append(res4)
                                listadoReporteria.append(auxReporteria)
                                auxReporteria = []
                                validarReporte()
                            else:
                                aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                                errores.append(aux) 
                                auxReporteria = []
                                popPila()  
                        else:
                            aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()  
                    else:
                        aux = [pila[0][0], 'Se esperaba una cadena o un valor númerico.', 'Sintáctico', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        auxReporteria = []
                        popPila()                    
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ,', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [str(campo), 'No se encontro el campo indicado.', 'Ejecución', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()                
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarDATOS():
    global auxReporteria
    global listadoReporteria
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)
        res2 = validarParentesis(pila[0][0], 'c')
        if res2 == True:
            pila.pop(0)
            if pila[0][0] == ';':
                pila.pop(0)
                listadoReporteria.append(auxReporteria)
                auxReporteria = []
                validarReporte()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarSUMAR():
    global auxReporteria
    global listadoReporteria
    campo = ''
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            #auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            campo = pila[0][0]
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    res3 = buscarClave(darFormato(campo, 'Cadena'))#Obtiene la clave a la que se le va a ser la suma.
                    if res3[0] == True:
                        res4 = calcularSuma(res3[1])
                        if res4 != None:
                            auxReporteria.append(res4)
                            listadoReporteria.append(auxReporteria)
                            auxReporteria = []
                            validarReporte()
                        else:
                            #Si entra aquí encontro un valor tipo string(no se puede calcular la suma).
                            aux = [pila[0][0], 'Se esperaba un valor númerico.', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()
                    else:
                        aux = [str(campo), 'No se encontro el campo indicado.', 'Ejecución', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        auxReporteria = []
                        popPila()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()

def validarMAX():
    global auxReporteria
    global listadoReporteria
    campo = ''
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            #auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            campo = pila[0][0]
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    res3 = buscarClave(darFormato(campo, 'Cadena'))#Obtiene la clave donde se va a buscar el máximo
                    if res3[0] == True:
                        res4 = obtenerMax_Min(res3[1], 'max')
                        if res4 != None:
                            auxReporteria.append(str(res4))
                            listadoReporteria.append(auxReporteria)
                            auxReporteria = []
                            validarReporte()
                        else:
                            #Si entra aquí encontro un valor tipo string(no se puede encontrar el máximo).
                            aux = [pila[0][0], 'Se esperaba un valor númerico.', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()
                    else:
                        aux = [str(campo), 'No se encontro el campo indicado.', 'Ejecución', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        auxReporteria = []
                        popPila()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()    

def validarMIN():
    global auxReporteria
    global listadoReporteria
    campo = ''
    res = validarParentesis(pila[0][0], 'a')
    if res == True:
        pila.pop(0)#Elimina el parentesis de la apertura.
        if pila[0][1] == "Cadena":
            #auxReporteria.append(darFormato(pila[0][0], pila[0][1]))
            campo = pila[0][0]
            pila.pop(0)
            res2 = validarParentesis(pila[0][0], 'c')
            if res2 == True:
                pila.pop(0)#Elimina el parentesis de cierre.
                if pila[0][0] == ';':
                    pila.pop(0)
                    res3 = buscarClave(darFormato(campo, 'Cadena'))#Obtiene la clave donde se va a buscar el máximo
                    if res3[0] == True:
                        res4 = obtenerMax_Min(res3[1], 'min')
                        if res4 != None:
                            auxReporteria.append(str(res4))
                            listadoReporteria.append(auxReporteria)
                            auxReporteria = []
                            validarReporte()
                        else:
                            #Si entra aquí encontro un valor tipo string(no se puede encontrar el máximo).
                            aux = [pila[0][0], 'Se esperaba un valor númerico.', 'Sintáctico', pila[0][2], pila[0][3]]
                            errores.append(aux) 
                            auxReporteria = []
                            popPila()
                    else:
                        aux = [str(campo), 'No se encontro el campo indicado.', 'Ejecución', pila[0][2], pila[0][3]]
                        errores.append(aux) 
                        auxReporteria = []
                        popPila()
                else:
                    aux = [pila[0][0], 'Se esperaba el símbolo ;', 'Sintáctico', pila[0][2], pila[0][3]]
                    errores.append(aux) 
                    auxReporteria = []
                    popPila()
            else:
                aux = [pila[0][0], 'Se esperaba el símbolo )', 'Sintáctico', pila[0][2], pila[0][3]]
                errores.append(aux) 
                auxReporteria = []
                popPila()
        else:
            aux = [pila[0][0], 'Se esperaba el token Cadena', 'Sintáctico', pila[0][2], pila[0][3]]
            errores.append(aux) 
            auxReporteria = []
            popPila()
    else:
        aux = [pila[0][0], 'Se esperaba el símbolo (', 'Sintáctico', pila[0][2], pila[0][3]]
        errores.append(aux) 
        auxReporteria = []
        popPila()


def buscarClave(campo):
    for i in range(len(listadoClaves)):
        if campo == listadoClaves[i]:
            respuesta = [True, int(i)]
            return respuesta
    respuesta = [False]
    return respuesta   

def calcularPromedio(posicion):
    sumatoria = 0
    numeroRegistros = len(listadoRegistros)
    promedio = 0
    error = False
    for i in range(len(listadoRegistros)):
        if type(listadoRegistros[i][posicion]) is int:
            sumatoria += listadoRegistros[i][posicion]
        elif type(listadoRegistros[i][posicion]) is float:
            sumatoria += listadoRegistros[i][posicion]
        elif type(listadoRegistros[i][posicion]) is str:
            error = True
            break
    if error == False:
        promedio = sumatoria /  numeroRegistros
    else:
        promedio = None
    return promedio

def calcularContarsi(posicion, valor):
    cantidad = 0
    for i in range(len(listadoRegistros)):
        if listadoRegistros[i][posicion] == valor:
            cantidad += 1
    return cantidad   

def calcularSuma(posicion):
    suma = 0
    error = False
    for i in range(len(listadoRegistros)):
        if type(listadoRegistros[i][posicion]) is int:
            suma += listadoRegistros[i][posicion]
        elif type(listadoRegistros[i][posicion]) is float:
            suma += listadoRegistros[i][posicion]
        elif type(listadoRegistros[i][posicion]) is str:
            error = True
            break
    if error == True:
        suma = None
    return suma

def obtenerMax_Min(posicion, modo):
    listado = []
    if modo == 'max':
        encontroString = False
        for i in range(len(listadoRegistros)):
            if type(listadoRegistros[i][posicion]) is str:
                encontroString = True
                break
        if encontroString == False:
            for elemento in listadoRegistros:
                listado.append(elemento[posicion])
            #Ordenando en forma ascedente
            for i in range(len(listado)-1):
                for j in range(len(listado)-1):
                    if listado[j] > listado[j+1]:
                        tmp = listado[j]
                        listado[j] = listado[j+1]
                        listado[j+1] = tmp
            print(listado)
            return listado[-1] #Devuelve la última posición
        else:
            return None
    elif modo == 'min':
        encontroString = False
        for i in range(len(listadoRegistros)):
            if type(listadoRegistros[i][posicion]) is str:
                encontroString = True
                break
        if encontroString == False:
            for elemento in listadoRegistros:
                listado.append(elemento[posicion])
            #Ordenando en forma ascedente
            for i in range(len(listado)-1):
                for j in range(len(listado)-1):
                    if listado[j] > listado[j+1]:
                        tmp = listado[j]
                        listado[j] = listado[j+1]
                        listado[j+1] = tmp
            print(listado)
            return listado[0] #Devuelve la primera posición
        else:
            return None        