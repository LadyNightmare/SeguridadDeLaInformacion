from Crypto.Cipher import PKCS1_OAEP, DES, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pss
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import base64
import json
from socket_class import SOCKET_SIMPLE_TCP

# Parametros
key_b_t = b'FEDCBA9876543210'
BLOCK_SIZE_AES = 16

# Abre una conexion a B
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 4321)
socket.conectar()

# M: Obtengo clave de secion K_AB
file = open("E_BT(K_AB, Alice).txt", "rb")
datos = file.read()
descipher_aes_a_b = AES.new(key_b_t, AES.MODE_ECB)
json_t_b = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("A->M: " + json_t_b)
msg_t_b = json.loads(json_t_b)
t_k_ab, t_alice = msg_t_b
t_k_ab = bytearray.fromhex(t_k_ab)

# M->B: E_BT(K_AB, Alice)
socket.enviar(datos)
print("M->B: ", datos)

# B->M: E_AB(Rb)
# M: Rb - 1
datos = socket.recibir()
print("B->M: E_AB(Rb)")
descipher_aes_a_b = AES.new(t_k_ab, AES.MODE_ECB)
b_random = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES)
elem = bytearray(b_random)
elem[7] = elem[7] - 1
b_random = bytes(elem)

# M->B: E_AB(Rb - 1)
cipher_aes_a_b = AES.new(t_k_ab, AES.MODE_ECB)
msg_enc = cipher_aes_a_b.encrypt(pad(b_random, BLOCK_SIZE_AES))
print("M->B: E_AB(Rb - 1)")
socket.enviar(msg_enc)

msg_enc = cipher_aes_a_b.encrypt(pad("Alice".encode("utf-8"), BLOCK_SIZE_AES))
print("M->B: E_AB(Alice)")
socket.enviar(msg_enc)

datos = socket.recibir()
bob = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("B->M: E_AB(Bob)")


socket.cerrar()