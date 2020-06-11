import os
import time
import config


def existfile(filename):
	if os.path.exists(filename) and os.path.isfile(filename) and os.access(filename, os.W_OK):
		return True;
	#endif
	return False;
#enddef

def removefile(filename):
	if existfile(filename):
		os.remove(filename)
#enddef

def makedirsforfile(filename):
	dirname = filename[:filename.rfind('/')]
	if os.path.exists(dirname) == False:
		os.makedirs(dirname)
	#endif
#enddef
