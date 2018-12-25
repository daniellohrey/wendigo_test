import sys
import imp
import netrc
from github3 import login

class ReImp(object):
        def __init__(self):
                self.code = ""

        def find_module(self, fullname, path = None):
		print fullname
		fullname = fullname.split(".")[-1]
                lib = search_file(fullname, "modules")
                if lib is not None:
                        self.code = lib
                        return self
                return None

        def load_module(self, name):
                module = imp.new_module(name)
                exec self.code in module.__dict__
                sys.modules[name] = module
                return module

def connect():
        gh = login(token = "9ea5bb8f5df4c1582a2083d208210c6b183bba56")
        repo = gh.repository("daniellohrey", "wendigo_test")
        return repo

def search_file(fullname, search):
	#print "search: " + fullname + " in: " + search
	repo = connect()
	cont = repo.directory_contents(search)
	for fn, c in cont:
		#print "fn: " + fn + " c: " + c.path + " " + c.type
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

sys.meta_path = [ReImp()]
exec("from xml import etree")
