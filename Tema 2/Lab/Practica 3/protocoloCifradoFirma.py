from RSA import RSA_OBJECT
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Creamos A y B con sus respectivas claves
A = RSA_OBJECT()
A.create_KeyPair()
B = RSA_OBJECT()
B.create_KeyPair()

# Inicializamos el mensaje y lo ciframos con la clave pública de B
mensaje = "Hola Amigos de la Seguridad"
print(mensaje)
c = B.cifrar(mensaje.encode("utf-8"))
print(c)

# Firmamos el cifrado anterior con la clave privada de A
s = A.firmar(c)
print(s)

# Guardamos tanto c como s en un fichero (lo mandamos a B)
file_out = open("file.txt", "wb")
file_out.write(s)
file_out.write(c)
file_out.close()

# Obtenemos c y s
file_in = open("file.txt", "rb")
s_in = file_in.read(256)
c_in = file_in.read()
file_in.close()

# Comprobamos

if A.comprobar(c_in, s_in):
    mensaje = B.descifrar(c_in).decode("utf-8")
    print(mensaje)
else:
    print("La firma es invalida")

class AES_CIPHER:

    BLOCK_SIZE_AES = 16

    def __init__(self, key):
        self.key = key

    def cifrar(self, cadena, IV):
        cifradoAES = AES.new(self.key, AES.MODE_CBC, IV)
        textoCifrado = cifradoAES.encrypt(pad(cadena.encode("utf-8"),type(self).BLOCK_SIZE_AES))
        return textoCifrado

    def descifrar(self, cifrado, IV):
        descifradoAES = AES.new(self.key, AES.MODE_CBC, IV)
        textoDescifrado = unpad(descifradoAES.decrypt(cifrado), type(self).BLOCK_SIZE_AES).decode("utf-8","ignore")
        return textoDescifrado


print("Compartimos una clave de sesión")

A = RSA_OBJECT()
A.create_KeyPair()
B = RSA_OBJECT()
B.create_KeyPair()

mensaje = get_random_bytes(16)
cifrado = B.cifrar(mensaje)
firma = A.firmar(cifrado)

file_out = open("file.txt", "wb")
file_out.write(firma)
file_out.write(cifrado)
file_out.close()

encrypted_file = open("file.txt", "rb")
encrypted_signature = encrypted_file.read(256)
encrypted_crypted = encrypted_file.read(256)

if A.comprobar(encrypted_crypted, encrypted_signature):
    key = B.descifrar(encrypted_crypted)
    IV = get_random_bytes(16)
    datos = "Hola amigos de seguridad"
    d = AES_CIPHER(key)
    cifrado = d.cifrar(datos, IV)
    print(cifrado)
    descifrado = d.descifrar(cifrado,IV)
    print(descifrado)
else:
    print("La firma es invalida")