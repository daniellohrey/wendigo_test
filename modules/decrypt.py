import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

data = "IDBhqY/Nxqvzr/sTFkaCHYej0HIVeKg0MkP6unDuHRwdMtnMlOJ72NQSqPzmAMfxMKezB78/dlJvnBqpvP7GlLfhvpIyVc8Oe5f9joMdUuw53NwfGXWYbWawe45qryIWYOcUm+XiRSVqz+1XVd9rdS1ErKvC67dsE/qQtwLQ1ElgfDBEOO5f6XmXZKLZsahl8XG5+FZ7Hiybyqj369TL36iwK5HX/R9OJ3APb3K/VwjuWQuMTKqySrqESf+Pdw5D4/ucFgZU6Rp+j6kgsn+EOxPKqsdRIKl+eu42KeFmahCl0yfhQw0xlCXpl9irAkcFjQzMTndMYaaZ1j6XESisYZ7QArzdErAxbMhfc/pMVUx1Dv7ZAdHiG5VuXJLyAeUZOynoN7bAMagnpd9bfuD7XY57s+5CQV4WQhXUGO2tm3A1yaJUqIhXu/T1tqUt50LScEiYlqDlHa9veLx0Muo8W8xWL8W0wqF4cG7/boHi6XmFsFs+6dM728rGbdYmi57X7a/OxDzwGkhllBvkqqXnwdCdwiadnk82ydnlWhUYEm95qaymvFsQhoXYTkdPdYfQVkzwFG+o6S4ybtZJHhru1nKo9PB59Fwz5E2i1tyb5EUbzstvElq1uWajNmIH5tFouavTXKvlfq7+qUkxZJ3jf2YvOTJ5/38P+4raBBz/3KE="

f = open("pk.o", "r")
priv = f.read()
f.close()

data = base64.b64decode(data)

size = 256
offset = 0
decrypted = ""

key = RSA.importKey(priv)
key = PKCS1_OAEP.new(key)

while offset < len(data):
	decrypted += key.decrypt(data[offset:offset + size])
	offset += size

plain = zlib.decompress(decrypted)
print plain
