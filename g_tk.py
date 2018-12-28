import sys
import time
from base64 import b64encode
from getpass import getpass
from github3 import authorize

p = getpass("GitHub password: ")
auth = authorize("daniellohrey", p, scopes = ["public_repo"], 
	note = str(int(time.time())))

if len(sys.argv) > 1:
	print b64encode(auth.token)
else:
	print auth.token

with open("tk.o", "w") as f:
	f.write(str(auth.id))
