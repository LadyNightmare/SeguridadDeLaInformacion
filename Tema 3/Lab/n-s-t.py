from Crypto.Cipher import PKCS1_OAEP, DES, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pss
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import base64
import json
from socket_class import SOCKET_SIMPLE_TCP


key_a_t = b'0123456789ABCDEF'
key_b_t = b'FEDCBA9876543210'
BLOCK_SIZE_AES = 16


socket = SOCKET_SIMPLE_TCP('127.0.0.1', 12354)
socket.escuchar()
print("Socket creado, esperando nueva conexión.")


datos = socket.recibir()
json_a_t = datos.decode("utf-8" ,"ignore")
print("A -> T: " + json_a_t)
msg_a_t = json.loads(json_a_t)


t_alice, t_bob, t_random = msg_a_t
t_random = bytearray.fromhex(t_random)

key_a_b = get_random_bytes(16)


msg_t_a = []
msg_t_a.append(t_random.hex())
msg_t_a.append(t_bob)
msg_t_a.append(key_a_b.hex())
msg_t_b = []
msg_t_b.append(key_a_b.hex())
msg_t_b.append(t_alice)
cipher_aes_b_t = AES.new(key_b_t, AES.MODE_ECB)
msg_t_b_enc = cipher_aes_b_t.encrypt(pad(json.dumps(msg_t_b).encode("utf-8"),BLOCK_SIZE_AES))
msg_t_a.append(msg_t_b_enc.hex())


json_t_a = json.dumps(msg_t_a)
cipher_aes_a_t = AES.new(key_a_t, AES.MODE_ECB)
datos =  cipher_aes_a_t.encrypt(pad(json_t_a.encode("utf-8"),BLOCK_SIZE_AES))

print("T -> A: " + json_t_a)
socket.enviar(datos)

socket.cerrar()
print("Socket cerrado. Se ha terminado la conexión.")
