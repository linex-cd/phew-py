import os
import time
import config

def readfile(filename):
	
	f = open(filename, "r");
	if f == False:
		return None;
	#endif
	
	text = "";
	
	for line in f.readlines():
		text = text + line;
	#endfor

	f.close();
	
	return text;
#enddef

def writefile(filename, text, mode = "w"):
	
	f = None;
	encoding = "UTF-8";
	if mode.find("b") >=0:
		encoding = None;
	#endif

	f = open(file = filename, mode = mode, encoding = encoding);

	f.write(text);
	f.close();
	pass;
#enddef

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
