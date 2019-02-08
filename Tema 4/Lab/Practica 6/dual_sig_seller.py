from socket_class import SOCKET_SIMPLE_TCP
from rsa_class import RSA_OBJECT
from aes_class import AES_CIPHER
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64
import json

# Recibe la informacion del cliente
###################################
# Crea el socket en 5555
print("Creando socket y escuchando...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5555)
socket.escuchar()

# Recibe los datos y cierra el socket
datos = socket.recibir()
json_vendedor = datos.decode("utf-8" ,"ignore")
socket.cerrar()

# Decodifica los datos
msg_cliente = json.loads(json_vendedor)
json_banco_cifrado_hex, IV_banco_hex, digital_envelope_hex, PIMD_hex, OI_vendedor, firma_dual_hex, pub_usuario_hex = msg_cliente

#####################################################
# A REALIZAR POR EL ALUMNO
#
# Comprobar que la informacion recibida por parte 
# del cliente es integra, considerando en este caso
# la firma dual computada por dicho cliente
######################################################
# Verif 1
OIMD_hex = SHA256.new(data=OI_vendedor.encode('utf-8')).hexdigest()

# PIMD_hex+OIMD_hex
msg = []
msg.append(PIMD_hex)
msg.append(OIMD_hex)
json_msg = json.dumps(msg)
# Hash PIMD_hex+OIMD_hex
POMD = SHA256.new(data=json_msg.encode('utf-8')).digest()

# Verif 2
RSA_Usuario = RSA_OBJECT()
RSA_Usuario.load_PublicKey("rsa_key.pub")


if not RSA_Usuario.verify(POMD, bytes.fromhex(firma_dual_hex)):
    print("firma dual incorrecta")
    exit()
print("VENDEDOR: " + OI_vendedor)

#banco (PI, firma dual, OIMD)
msg_banco = []
msg_banco.append(json_banco_cifrado_hex)
msg_banco.append(IV_banco_hex)
msg_banco.append(digital_envelope_hex)
msg_banco.append(pub_usuario_hex)
json_banco = json.dumps(msg_banco)

# Abr Socket
socketBanco = SOCKET_SIMPLE_TCP('127.0.0.1', 5556)
socketBanco.conectar()
# Envio info
print("Vendedor -> Banco: mensaje")
socketBanco.enviar(json_banco.encode("utf-8"))
# Cierro Socket
socketBanco.cerrar()
print("Vendedor finaliza transaccion")
