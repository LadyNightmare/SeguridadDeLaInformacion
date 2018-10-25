class DES_CIPHER:

 BLOCK_SIZE_DES = 8 # DES: Bloque de 64 bits

 def __init__(self, key):
     key = get_random_bytes(8)  # Clave aleatoria de 64 bits
     IV = get_random_bytes(8) # IV aleatorio de 64 bits

 def cifrar_CBC(self, cadena, IV):
     # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
     cipher = DES.new(key, DES.MODE_CBC, IV)

     # Ciframos, haciendo que data sea multiplo del tamaño de bloque
     ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE_DES))

 def descifrar_CBC(self, cifrado, IV):
     # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
     # Ambos, cifrado y descifrado, se crean de la misma forma
     decipher_des = DES.new(key, DES.MODE_CBC, IV)

     # Desciframos, eliminamos el padding, y recuperamos la cadena
     new_data = unpad(decipher_des.decrypt(ciphertext), BLOCK_SIZE_DES).decode("utf-8", "ignore")

key = get_random_bytes(8) # Clave aleatoria de 64 bits
IV = get_random_bytes(8) # IV aleatorio de 64 bits

datos = "Hola Mundo con DES en modo CBC"
d = DES_CIPHER(key)
cifrado = d.cifrar_CBC(datos, IV)
descifrado = d.descifrar_CBC(cifrado, IV)