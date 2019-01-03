import sys
import imp
import StringIO
from github3 import login

def search_file(fullname, search):
	gh = login(token = "f58c564505301a23df98092f96c9696075a0aba9")
	repo = gh.repository("daniellohrey", "wendigo_test")
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
			s_io = StringIO.StringIO(contents)
		else:
			return None
		suffixes = (".py", "r", imp.PY_SOURCE)
		pathname = pathname + "/" + mod
		try:
			n_mod = imp.new_module(modname)
			exec contents in n_mod.__dict__
			sys.modules[modname] = n_mod
		finally:
			s_io.close()
	return sys.modules[fullname]

try:
	yay = my_load("xml.etree.ElementTree")
	print str(yay)
except Exception as e:
	print str(e)
