from getpass import getpass
from github3 import login

gh = login("daniellohrey", getpass("GitHub password:"))

with open("tk.o", "r") as f:
	id = f.read()

auth = gh.authorization(int(id))
if auth.delete():
	print "deleted"
else:
	print "failed to delete"
