def cifradoCesarAlfabetoInglesMAY(cadena):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) + 3) % 26) + 65
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    # devuelve el resultado
    return resultado

def descifradoCesarAlfabetoInglesMAY(cadena):
    resultado = ''
    i = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) - 3) % 26) + 65
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    return resultado

def cifradoCesarAlfabetoIngles(cadena):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) + 3) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = (((ordenClaro - 97) + 3) % 26) + 97
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    # devuelve el resultado
    return resultado

def descifradoCesarAlfabetoIngles(cadena):
    resultado = ''
    i = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) - 3) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = (((ordenClaro - 97) - 3) % 26) + 97
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    return resultado

def cifradoCesarAlfabetoInglesGeneral(cadena, k):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) + k) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = (((ordenClaro - 97) + k) % 26) + 97
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    # devuelve el resultado
    return resultado

def descifradoCesarAlfabetoInglesGeneral(cadena, k):
    resultado = ''
    i = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = (((ordenClaro - 65) - k) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = (((ordenClaro - 97) - k) % 26) + 97
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
    return resultado

claroCESAR = 'VENI VIDI VINCI ZETA'
print("Mensaje a cifrar: " +claroCESAR)
cifradoCESAR = cifradoCesarAlfabetoInglesMAY(claroCESAR)
print(cifradoCESAR + "\n")
print("Mensaje a descifrar: " + cifradoCESAR)
descifradoCESAR = descifradoCesarAlfabetoInglesMAY(cifradoCESAR)
print(descifradoCESAR + "\n")

claroCESARmixture = 'VEnI VIDI vinCi zeta'
print("Mensaje a cifrar: " +claroCESARmixture)
cifradoCESARmixture = cifradoCesarAlfabetoIngles(claroCESARmixture)
print(cifradoCESARmixture + "\n")
print("Mensaje a descifrar: " + cifradoCESARmixture)
descifradoCESARmixture = descifradoCesarAlfabetoIngles(cifradoCESARmixture)
print(descifradoCESARmixture + "\n")

claroCESARgeneral = 'VEnI VIDI vinCi zeta'
print("Mensaje a cifrar: " +claroCESARgeneral)
cifradoCESARgeneral = cifradoCesarAlfabetoInglesGeneral(claroCESARgeneral, 5)
print(cifradoCESARgeneral + "\n")
print("Mensaje a descifrar: " + cifradoCESARgeneral)
descifradoCESARgeneral = descifradoCesarAlfabetoInglesGeneral(cifradoCESARgeneral, 5)
print(descifradoCESARgeneral + "\n")