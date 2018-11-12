from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter
import base64

class DES_CIPHER:

    BLOCK_SIZE_DES = 8 # DES: Bloque de 64 bits

    def __init__(self, key):
        self.key = key  # Clave aleatoria de 64 bits

    def cifrar_CBC(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = DES.new(key, DES.MODE_CBC, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_DES))

        return ciphertext

    def descifrar_CBC(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_des = DES.new(key, DES.MODE_CBC, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_des.decrypt(cifrado), self.BLOCK_SIZE_DES).decode("utf-8", "ignore")

        return new_data

key = get_random_bytes(8) # Clave aleatoria de 64 bits
IV = get_random_bytes(8) # IV aleatorio de 64 bits
datos = "Hola Mundo con DES en modo CBC".encode("utf-8")
print(datos)
d = DES_CIPHER(key)
cifrado = d.cifrar_CBC(datos, IV)
print(cifrado)
encoded_ciphertext = base64.b64encode(cifrado)
print(encoded_ciphertext)
descifrado = d.descifrar_CBC(cifrado, IV)
print(descifrado)

