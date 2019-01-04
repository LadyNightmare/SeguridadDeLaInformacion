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
key_a_t = b'0123456789ABCDEF'
BLOCK_SIZE_AES = 16

# Abre una conexion a T
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5555)
socket.conectar()

# A: Crear campos
a_alice = "Alice"
a_bob = "Bob"
a_random = get_random_bytes(8)

# A: msg_a_t = Alice, Bob, Ra
msg_a_t = []
msg_a_t.append("Alice")
msg_a_t.append("Bob")
msg_a_t.append(a_random.hex())
json_a_t = json.dumps(msg_a_t)

# A->T: msg_a_t
print("A->T: " + json_a_t)
socket.enviar(json_a_t.encode("utf-8"))

# T->A: E_AT(Ra, Bob, K_AB, E_BT(K_AB, Alice))
# A: Descifrar msg_t_a
datos = socket.recibir()
decipher_aes_a_t = AES.new(key_a_t, AES.MODE_ECB)
json_t_a = unpad(decipher_aes_a_t.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("T->A (Clear): " + json_t_a)
msg_t_a = json.loads(json_t_a)

# A: Comprobar campos de msg_t_a
t_random, t_bob, t_k_ab, t_bt = msg_t_a
t_random = bytearray.fromhex(t_random)
t_k_ab = bytearray.fromhex(t_k_ab)
if (a_random != t_random):
    print("ERROR: Nonce Equivocado")
    socket.cerrar()
    exit()
if (a_bob != t_bob):
    print("ERROR: Receptor incorrecto")
    socket.cerrar()
    exit()

# Hemos terminado con la conexion con T, podemos cerrar el socket
socket.cerrar()

#####################################################################
# COMPLETAR: CONTACTAR CON BOB, SEGUIR EL PROTOCOLO NEEDHAM-SCHROEDER
#####################################################################

