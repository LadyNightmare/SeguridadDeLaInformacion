from Crypto.Cipher import PKCS1_OAEP, DES, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pss
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import base64
import json
from socket_class import SOCKET_SIMPLE_TCP


key_b_t = b'FEDCBA9876543210'
BLOCK_SIZE_AES = 16


socket = SOCKET_SIMPLE_TCP('127.0.0.1', 12543)
socket.escuchar()
print("Socket creado. Esperando conexión.")


datos = socket.recibir()
descipher_aes_a_b = AES.new(key_b_t, AES.MODE_ECB)
json_t_b = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("A -> B: " + json_t_b)
msg_t_b = json.loads(json_t_b)


t_k_ab, t_alice = msg_t_b
t_k_ab = bytearray.fromhex(t_k_ab)


b_random = get_random_bytes(8)
cipher_aes_a_b = AES.new(t_k_ab, AES.MODE_ECB)
msg_enc = cipher_aes_a_b.encrypt(pad(b_random, BLOCK_SIZE_AES))
print("B -> A: E_AB(Rb)")
socket.enviar(msg_enc)


datos = socket.recibir()
descipher_aes_a_b = AES.new(t_k_ab, AES.MODE_ECB)
ramdon_ab = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES)

if(int.from_bytes(ramdon_ab, byteorder='big') != int.from_bytes(b_random, byteorder='big') - 1):
	print("Error: El Nonce está equivocado.")
	socket.cerrar()
	print("Se ha cerrado la conexión.")
	exit()

print("B -> A: E_AB(Rb - 1)")
datos = socket.recibir()
alice = unpad(descipher_aes_a_b.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("A -> B: E_AB(%s)" % alice)

msg_enc = cipher_aes_a_b.encrypt(pad("Bob".encode("utf-8"), BLOCK_SIZE_AES))
socket.enviar(msg_enc)
print("B -> A: E_AB(Bob)")
