import sys
import imp
import netrc
from github3 import login

class ReImp(object):
        def __init__(self):
                self.code = ""

        def find_module(self, fullname, path = None):
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
        gh = login(token = "106f7d2dc19ac1c237d009db362f8d50137d2363")
        repo = gh.repository("daniellohrey", "wendigo_test")
        return repo

def search_file(fullname, search):
	print "search: " + fullname + " in: " + search
	repo = connect()
	cont = repo.directory_contents(search)
	for fn, c in cont:
		print "fn: " + fn + " c: " + c.path + " " + c.type
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
#implement a stack of imports, and a list of previous imports to skip
#import whole package recursively
def main ():
	import xml
	for mod in xml.__dict__["__all__"]:
		exec("import %s" % mod)
	#try to use a bunch of things from the modules
main()
