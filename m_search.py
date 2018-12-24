import sys
from github3 import login

class ReImp(object):
        def __init__(self):
                self.code = ""

        def find_module(self, fullname, path = None): #get file from github
                lib = search_file(fullname)
                if lib is not None:
                        self.code = lib
                        return self
                return None

        def load_module(self, name): #load file into new module
                module = imp.new_module(name)
                exec self.code in module.__dict__
                sys.modules[name] = module
                return module

def connect():
        gh = login(token = "39cf79eaf35e6fe808b9f82ac877cb4e71d260e2")
        repo = gh.repository("daniellohrey", "wendigo_test")
        return repo

def search_file(fullname):
	print "searching for: " + fullname
        try:
                repo = connect()
		print repo.name
                branch = repo.branches().next()
		print branch.name
		print type(branch.commit)
		print "made1"
		print str(branch.commit.tree)
		print "made2"
		print str(branch.commit.commit)
		print "made3"
		print str(branch.commit.commit.tree)
		print "made4"
                tree = branch.commit.commit.tree
		print str(tree)
		try:
			print "tree: " + tree
			print "tree recurse: " + tree.recurse()
			print "tree resurse.tree: " + tree.recurse().tree
		except Exception as e:
			print "couldnt print tree: " + str(e)
                root = repo.create_tree([{"path":"modules", "mode":"040000",
                        "type":"tree", "sha":tree.sha}])
                for name in root.recurse().tree:
			print "file: " + name
                        n = name.split("/")
			n = n[1:]
			n = "/".join(n)
			print "file post cut: " + n
			if fullname in n:
                                f = repo.file_contents(n).decoded
				try:
					print "top of file: " + f[0:30]
				except Exception as e:
					print "couldnt print file: " + str(e)
				return f
                return None
        except Exception as e:
		print "hit exception: " + str(e)
                return None

sys.meta_path = [ReImp()]
exec("import xml")
print "import success"
print str(xml.__dict__)
