from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter
import base64

class DES_CIPHER:

    BLOCK_SIZE_AES = 16 # DES: Bloque de 128 bits

    def __init__(self, key):
        self.key = key  # Clave aleatoria de 128 bits

    def cifrar_AES_CBC(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = AES.new(key, AES.MODE_CBC, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_AES))

        return ciphertext

    def descifrar_AES_CBC(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(key, AES.MODE_CBC, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(ciphertext), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")

        return new_data

    def cifrar_AES_ECB(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = AES.new(key, AES.MODE_ECB, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_AES))

        return ciphertext

    def descifrar_AES_ECB(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(key, AES.MODE_ECB, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(ciphertext), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")

        return new_data

    def cifrar_AES_CTR(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = AES.new(key, AES.MODE_CTR, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_AES))

        return ciphertext

    def descifrar_AES_CTR(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(key, AES.MODE_CTR, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(ciphertext), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")

        return new_data

    def cifrar_AES_OFB(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = AES.new(key, AES.MODE_OFB, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_AES))

        return ciphertext

    def descifrar_AES_OFB(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(key, AES.MODE_OFB, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(ciphertext), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")

        return new_data

    def cifrar_AES_CFB(self, cadena, IV):
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = AES.new(key, AES.MODE_CFB, IV)

        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(datos, self.BLOCK_SIZE_AES))

        return ciphertext

    def descifrar_AES_CFB(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(key, AES.MODE_CFB, IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(ciphertext), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")

        return new_data



key = get_random_bytes(16) # Clave aleatoria de 128 bits
IV = get_random_bytes(16) # IV aleatorio de 128 bits
datos = "Hola Mundo con AES en modo CBC"
d = DES_CIPHER(key)
cifrado = d.cifrar_AES_CBC(datos, IV)
descifrado = d.descifrar_AES_CBC(cifrado, IV)

