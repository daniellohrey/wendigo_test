import sys
import imp
from github3 import login

def search_file(fullname, search):
	repo = connect()
	cont = repo.directory_contents(search)
	for fn, c in cont:
		if "dir" in c.type:
			s = search_file(fullname, c.path)
			if s is not None:
				return s
			else:
				continue
		#potential bug in matching with sub sub packages
		if fullname in fn or (fullname in c.path and "__init__" in fn):
			return repo.file_contents(c.path).decoded
	return None

#returns handle to module (such as with "import module as name")
def my_load(fullname):
	name = fullname.split(".")
	pathname = "modules"
	modname = ""
	for mod in name:
		if modname:
			modname = modname + "." + mod
		else:
			modname = mod
		contents = search_file(mod, pathname)
		if contents:
			with open("temp.py", "w") as f:
				f.write(contents)
		else:
			return None
		suffixes = (".py", "r", imp.PY_SOURCE)
		pathname = pathname + "/" + mod
		file = open("temp.py", "r")
		try:
			sys.modules[modname] = imp.load_module(modname, file, 
								pathname, suffixes)
		finally:
			file.close()
	return sys.modules[fullname]
