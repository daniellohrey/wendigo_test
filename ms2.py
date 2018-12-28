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
        gh = login(token = "84db4d86dbbbc089c99a9d1524a5bc8364b80032")
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
#implement a stack of imports, and a list of previous imports to skip
#import whole package recursively
def main ():
	import xml
	for mod in xml.__dict__["__all__"]:
		exec("import %s" % mod)
	#try:
	#	import xml #pass
	#except:
	#	print "fail 1"
	try:
		import xml.etree
	except Exception as e:
		print "fail 1.2"
		print str(e)
	#try:
	#	print xml.etree.ElementTree
	#except:
	#	print "fail 3"
	#try:
	#	import etree #pass
	#except:
	#	print "fail 4"
	#try:
	#	import etree.ElementTree
	#except:
	#	print "fail 5"
	try:
		import ElementTree
	except Exception as e:
		print "fail 1.6"
		print str(e)
	try:
		tree = xml.etree.ElementTree.parse("xmltest.xml")
	except Exception as e:
		print "fail 2.1"
		print str(e)
	try:
		tree = etree.ElementTree.parse("xmltest.xml")
	except Exception as e:
		print "fail 2.2"
		print str(e)
	try:
		tree = ElementTree.parse("xmltest.xml")
	except Exception as e:
		print "fail 2.3"
		print str(e)
	try:
		et = etree.ElementTree()
	except Exception as e:
		print "fail 2.4"
		print str(e)
main()
