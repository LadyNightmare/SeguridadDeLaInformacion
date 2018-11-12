from Crypto.Hash import SHA512, SHA3_256, HMAC, BLAKE2s

################## Ejercicio 1.a ##################
fileName = "Nombre y apellidos.txt"
file = open(fileName, "rb")
fileContent = file.read()
hashObj = SHA512.new(data=fileContent)

print("Apartado a")
print("    DIGEST: '%s'" % hashObj.digest())
print("    HEXDIGEST: '%s'\n" % hashObj.hexdigest())
file.close()

################## Ejercicio 1.b ##################
fileName = "Nombre y apellidos.txt"
key = b'S3cr3tK3y'
file = open(fileName, "rb")
fileContent = file.read()
hmacObj = HMAC.new(key, digestmod=SHA512)
hmacObj.update(fileContent)

print("Apartado b")
print("    DIGEST: '%s'" % hmacObj.digest())
print("    HEXDIGEST: '%s'\n" % hmacObj.hexdigest())

hmacComp = HMAC.new(key, digestmod=SHA512)
hmacComp.update(fileContent)
try:
	hmacComp.hexverify(hmacObj.hexdigest())
	print("El mensaje '%s' es auténtico\n" % fileContent)
except ValueError:
	print("El mensaje o la clave no son auténticos\n")
file.close()

################## Ejercicio 1.c ##################
fileName = "Nombre y apellidos.docx"
file = open(fileName, "rb")
hashObj = SHA3_256.new()

while True:
	byteRead = file.read(4000)

	if(byteRead == b''):
		break

	hashObj.update(byteRead)

print("Apartado c")
print("    DIGEST: '%s'" % hashObj.digest())
print("    HEXDIGEST: '%s'\n" % hashObj.hexdigest())
file.close()

################## Ejercicio 2 ##################
# SHA-2 family compatible con HMAC
#
# SHA-3 family no es compatible debido a que no tiene el parametro block_size
#
# BLAKE2 no es compatible porque no es posible establecer el digest_size del BLAKE2 cuando uso HMAC