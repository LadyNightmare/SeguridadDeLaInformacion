from socket_class import SOCKET_SIMPLE_TCP
from rsa_class import RSA_OBJECT
from aes_class import AES_CIPHER
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64
import json

# Campos Basicos
################
OI_Str = "Licencia Windows, 1 PC"
PI_Str = "Tarjeta debito 101010101"
RSA_Usuario = RSA_OBJECT()
RSA_Usuario.create_KeyPair()

###################################################
# A REALIZAR POR EL ALUMNO
#
# Crear una firma dual: Sig(H(H(OI) || H(PI)))
# Las variables resultantes deben ser:
# - OIMD: Hash del OI
# - PIMD: Hash del PI
# - firma_dual: Resultado de la firma dual
###################################################


RSA_Usuario.save_PublicKey("rsa_key.pub")
RSA_Usuario.save_PrivateKey("rsa_key.pem", "password")
PIMD = SHA256.new(data=PI_Str.encode('utf-8')).digest()
OIMD = SHA256.new(data=OI_Str.encode('utf-8')).digest()

msg_comprador = []
msg_comprador.append(PIMD.hex())
msg_comprador.append(OIMD.hex())
json_comprador = json.dumps(msg_comprador)
POMD = SHA256.new(data=json_comprador.encode('utf-8')).digest()

firma_dual = RSA_Usuario.sign(POMD)

if RSA_Usuario.verify(POMD, firma_dual):
	print("Se ha verificado.")
else:
	print("No se ha podido verificar.")

msg_banco = []
msg_banco.append(PI_Str)
msg_banco.append(firma_dual.hex())
msg_banco.append(OIMD.hex())
json_banco = json.dumps(msg_banco)


IV_banco = get_random_bytes(16)
key_banco = get_random_bytes(16)
AES_Usuario = AES_CIPHER(key_banco)
json_banco_cifrado = AES_Usuario.encrypt(json_banco, IV_banco)

RSA_Banco = RSA_OBJECT()
RSA_Banco.load_PublicKey("rsa_key.pub")
digital_envelope = RSA_Banco.encrypt(key_banco)

msg_vendedor = []
msg_vendedor.append(json_banco_cifrado.hex())
msg_vendedor.append(IV_banco.hex())
msg_vendedor.append(digital_envelope.hex())
msg_vendedor.append(PIMD.hex())
msg_vendedor.append(OI_Str)
msg_vendedor.append(firma_dual.hex())
msg_vendedor.append(RSA_Usuario.get_PublicKeyPEM().hex())
json_vendedor = json.dumps(msg_vendedor)


socketVendedor = SOCKET_SIMPLE_TCP('127.0.0.1', 5555)
socketVendedor.conectar()

socketVendedor.enviar(json_vendedor.encode("utf-8"))

socketVendedor.cerrar()
print("La transacción ha finalizado.")