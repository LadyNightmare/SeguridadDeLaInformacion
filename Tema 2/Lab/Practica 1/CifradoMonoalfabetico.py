def cifradoMonoalfabetico(cadena, clave, orden):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    j = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenClave = ord(clave[j % len(clave)])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = ((ordenClaro + ordenClave + orden) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = ((ordenClaro + ordenClave + orden) % 26) + 97
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
        j = j + 1
    # devuelve el resultado
    return resultado

def descifradoMonoalfabetico(cadena, clave, orden):
    resultado = ''
    i = 0
    j = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenClave = ord(clave[j % len(clave)])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if ordenClaro != 32:
            if (ordenClaro >= 65 and ordenClaro <= 90):
                ordenCifrado = ((ordenClaro - ordenClave - orden) % 26) + 65
            if (ordenClaro >= 97 and ordenClaro <= 122):
                ordenCifrado = ((ordenClaro - ordenClave - orden) % 26) + 97
            # Añade el caracter cifrado al resultado
            resultado = resultado + chr(ordenCifrado)
        i = i + 1
        j = j + 1
        # devuelve el resultado
    return resultado

claroMonoalfabetico = 'HOLAAMIGOS'
clave = 'CIFRA'
print("Texto a cifrar: " + claroMonoalfabetico)
textoCifrado = cifradoMonoalfabetico(claroMonoalfabetico, clave, 1)
print(textoCifrado + "\n")

print("Texto a descifrar: " + textoCifrado)
textoDescifrado = descifradoMonoalfabetico(textoCifrado, clave, 1)
print(textoDescifrado)