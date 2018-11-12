from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256

class RSA_OBJECT:
 def __init__(self):
     self.private_key = None
     self.public_key = None
 """Inicializa un objeto RSA, sin ninguna clave"""
 # Nota: Para comprobar si un objeto (no) ha sido inicializado, hay
 # que hacer "if self.public_key is None:"

 def create_KeyPair(self):
     self.private_key = RSA.generate(2048)
     self.public_key = self.private_key.publickey()
 """Crea un par de claves publico/privada, y las almacena dentro de la instancia"""
 def save_PrivateKey(self, file, password):
     key_cifrada = self.private_key.export_key(passphrase=password, pkcs=8, protection="scryptAndAES128-CBC")
     file_out = open(file, "wb")
     file_out.write(key_cifrada)
     file_out.close()
 """Guarda la clave privada self.private_key en un fichero file, usando una contraseña
password"""
 def load_PrivateKey(self, file, password):
     key_cifrada = open(file, "rb").read()
     self.private_key = RSA.import_key(key_cifrada, passphrase=password)
 """Carga la clave privada self.private_key de un fichero file, usando una contraseña
password"""
 def save_PublicKey(self, file):
     key_cifrada = self.public_key.export_key()
     file_out = open(file, "wb")
     file_out.write(key_cifrada)
     file_out.close()
 """Guarda la clave publica self.public_key en un fichero file"""
 def load_PublicKey(self, file):
     key_cifrada = open(file, "rb").read()
     self.public_key = RSA.import_key(key_cifrada)
 """Carga la clave publica self.public_key de un fichero file"""
 def cifrar(self, datos):
     if self.public_key is None:
         return None
     else:
         engineRSACifrado = PKCS1_OAEP.new(self.public_key)
         cifrado = engineRSACifrado.encrypt(datos)
         return cifrado
 """Cifra el parámetro datos (de tipo binario) con la clave self.public_key, y devuelve
 el resultado. En caso de error, se devuelve None"""
 def descifrar(self, cifrado):
     if self.private_key is None:
         return None
     else:
         engineRSADescifrado = PKCS1_OAEP.new(self.private_key)
         descifrado = engineRSADescifrado.decrypt(cifrado)
         return descifrado
 """Descrifra el parámetro cifrado (de tipo binario) con la clave self.private_key, y
Devuelve el resultado (de tipo binario). En caso de error, se devuelve None"""
 def firmar(self, datos):
     if self.private_key is None:
         return None
     else:
         h = SHA256.new(datos)
         print(h.hexdigest())
         signature = pss.new(self.private_key).sign(h)
         return signature
 """Firma el parámetro datos (de tipo binario) con la clave self.private_key, y devuelve
el resultado. En caso de error, se devuelve None."""
 def comprobar(self, text, signature):
     h = SHA256.new(text)
     print(h.hexdigest())
     verifier = pss.new(self.public_key)
     try:
         verifier.verify(h, signature)
         return True
     except (ValueError, TypeError):
         return False
 """Comprueba el parámetro text (de tipo binario) con respecto a una firma signature
 (de tipo binario), usando para ello la clave self.public_key.
 Devuelve True si la comprobacion es correcta, o False en caso contrario o
 en caso de error."""

 # Crear clave RSA
 # y guardar en ficheros la clave privada (protegida) y publica
 # password = "password"
 # private_file = "rsa_key.pem"
 # public_file = "rsa_key.pub"
 # RSA_key_creator = RSA_OBJECT()
 # RSA_key_creator.create_KeyPair()
 # RSA_key_creator.save_PrivateKey(private_file, password)
 # RSA_key_creator.save_PublicKey(public_file)
 # # Crea dos clases, una con la clave privada y otra con la clave publica
 # RSA_private = RSA_OBJECT()
 # RSA_public = RSA_OBJECT()
 # RSA_private.load_PrivateKey(private_file, password)
 # RSA_public.load_PublicKey(public_file)
 # # Cifrar y Descifrar con PKCS1 OAEP
 # cadena = "Lo desconocido es lo contrario de lo conocido. Pasalo."
 # cifrado = RSA_public.cifrar(cadena.encode("utf-8"))
 # print(cifrado)
 # descifrado = RSA_private.descifrar(cifrado).decode("utf-8")
 # print(descifrado)
 # # Firmar y comprobar con PKCS PSS
 # firma = RSA_private.firmar(cadena.encode("utf-8"))
 # if RSA_public.comprobar(cadena.encode("utf-8"), firma):
 #     print("La firma es valida")
 # else:
 #     print("La firma es invalida")