from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter
import base64

class AES_CIPHER:

    BLOCK_SIZE_AES = 16

    def __init__(self, key):
        """Inicializa las variables locales"""
        self.key = key

    def encrypt(self, cadena, IV):
        """Cifra el parametro cadena (de tipo String), y devuelve el texto cifrado binario"""
        datos = cadena.encode("utf-8")
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        return cipher.encrypt(pad(datos,type(self).BLOCK_SIZE_AES))

    def decrypt(self, datos, IV):
        """Cifra el parametro datos (de tipo binario), y devuelve la cadena en claro de tipo String"""
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        return unpad(cipher.decrypt(datos), type(self).BLOCK_SIZE_AES).decode("utf-8", "ignore")
