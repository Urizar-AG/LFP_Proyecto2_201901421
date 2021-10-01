
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
