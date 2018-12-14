#base64 encodes zipped/encrypted module files and pushes them to github

import base64
import sys
from github3 import login

if len(sys.argv) < 2:
	print "usage: %prog <file1 to push> [file2 to push] [...]"
	sys.exit(0)

mod = "config/"
usr = "daniellohrey"
repo = "wendigo_test"
tk = "ZWQ2YTVjZTQwYTU0NDM0MmNkMjJiZGI3MDUwN2MyMWRlMzIxNjBjMw=="
tk = base64.b64decode(tk)
i = 1
while i < len(sys.argv):
	try:
		#get contents of file
		f = open(sys.argv[i], "r")
		c = f.read()
		c = base64.b64encode(c)
		f.close()
	except:
		print "couldnt open file"
		i += 1
		continue

	#push to github
	try:
		gh = login(token = tk)
		rp = gh.repository(usr, repo)
	except:
		print "couldnt connect to github"
		i += 1
		continue

	fn = mod + sys.argv[i]
	cm = "upload" + sys.argv[i]
	try:
		rp.create_file(fn, cm, c) #file path, message, data
	except:
		#file already exists
		cm = "update" + sys.argv[i]
		rp.file_contents(fn).update(cm, c)
		i += 1
		continue

	i += 1
