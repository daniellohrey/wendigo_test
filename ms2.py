import sys
import imp
from github3 import login

#class ReImp(object):
#        def __init__(self):
#                self.code = ""
#
#        def find_module(self, fullname, path = None):
#                lib = search_file(fullname, "modules")
#                if lib is not None:
#                        self.code = lib
#                        return self
#                return None
#
#        def load_module(self, name):
#                module = imp.new_module(name)
#		exec self.code in module.__dict__
#		sys.modules[name] = module
#                return module

def connect():
        gh = login(token = "0fbdd665bf173c41648747115fb30f9e88985207")
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

def my_load(fullname):
	print "fullname: " + fullname
	name = fullname.split(".")
	print "name: " + str(name)
	pathname = "modules"
	modname = ""
	for mod in name:
		print "mod: " + mod
		if modname:
			modname = modname + "." + mod
		else:
			modname = mod
		print "modname: " + modname
		contents = search_file(mod, pathname)
		if contents:
			print "contents"
			with open("temp.py", "w") as f:
				f.write(contents)
		else:
			print "no contents"
		suffixes = (".py", "r", imp.PY_SOURCE)
		pathname = pathname + "/" + mod
		print "pathname: " + pathname
		file = open("temp.py", "r")
		try:
			#pathname can also be ""
			sys.modules[modname] = imp.load_module(modname, file, 
								pathname, suffixes)
			print "made it"
		except Exception as e:
			print "exception: " + str(e)
		finally:
			file.close()

#sys.meta_path = [ReImp()]
#implement a stack of imports, and a list of previous imports to skip
#import whole package recursively
def main ():
	#for mod in xml.__dict__["__all__"]:
	#	exec("import %s" % mod)
	my_load("xml.etree.ElementTree")
	tree = sys.modules["xml.etree.ElementTree"].parse("xmltest.xml")
	root = tree.getroot()
	print "xml tree root: " + root.tag
main()
