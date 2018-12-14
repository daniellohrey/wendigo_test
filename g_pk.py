#generates a new public/provate key pair and outputs the private key to file
#encodes and prints public key so it can easily be copied

from Crypto.PublicKey import RSA
import base64
import sys

new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

try:
	f = open("pk.o", "w")
except:
	print "couldnt open file"
	sys.exit()

f.write(private_key)
print base64.b64encode(public_key)
