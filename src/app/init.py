
import time
import json

import redis

from django.http import HttpResponse, HttpResponseRedirect, FileResponse


def redirect(url):
	
	return HttpResponseRedirect(url)

def response(code, msg, data):
	
	data = {"code":code, "msg": msg, "data": data}
	
	resp = HttpResponse(json.dumps(data), content_type='application/json')
	resp["Access-Control-Allow-Origin"] = "*"
	resp["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	resp["Access-Control-Max-Age"] = "1800"
	resp["Access-Control-Allow-Headers"] = "*"
	
	return resp

def responsefile(filename):
	
	downloadname = filename[filename.rfind('/')+1:]
	
	response = FileResponse(open(filename ,'rb'))
	response['Content-Type']='application/octet-stream'
	response['Content-Disposition']='attachment;filename="'+downloadname+'"'
	
	return response
	
import hashlib   
import base64   

def md5(src):
	m2 = hashlib.md5();
	m2.update(src);
	dest = m2.hexdigest();
	return dest;
#enddef

def encrypt(message):

	decrypted = b"abcdefghijklmnopqrstuvwxyz1234567890 "
	encrypted = b"0987654321qwertyuiopasdfghjklzxcvbnm "
	
	encrypt_table = bytes.maketrans(decrypted, encrypted)
	decrypt_table = bytes.maketrans(encrypted, decrypted)

	result = message.translate(encrypt_table)
	result = base64.b64encode(result.encode()).decode()
	result = result.translate(encrypt_table)
	
	return result
#enddef

def decrypt(message):

	decrypted = b"abcdefghijklmnopqrstuvwxyz1234567890 "
	encrypted = b"0987654321qwertyuiopasdfghjklzxcvbnm "
	
	encrypt_table = bytes.maketrans(decrypted, encrypted)
	decrypt_table = bytes.maketrans(encrypted, decrypted)
	
	result = message.translate(decrypt_table)
	result = base64.b64decode(result.encode()).decode()
	result = result.translate(decrypt_table)
	return result
	
#enddef

from os import W_OK as os_W_OK;
from os import access as os_access;
from os import remove as os_remove;
from os import makedirs as os_makedirs;
from os.path import join as os_path_exists;
from os.path import isfile as os_path_isfile;
from os.path import getsize as os_path_getsize;

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
	if mode.find("b") >= 0:
		encoding = None;
	#endif
	
	f = open(file = filename, mode = mode, encoding = encoding);
	
	f.write(text);
	f.close();
	pass;
#enddef

def existfile(filename):
	if os_path_exists(filename) and os_path_isfile(filename) and os_access(filename, os_W_OK):
		return True;
	#endif
	return False;
#enddef

def filesize(filename):
	if os_path_exists(filename) and os_path_isfile(filename) and os_access(filename, os_W_OK):
		return os_path_getsize(filename);
	#endif
	return 0;
#enddef


datapath = '/jobcenterdata/taskcache/'
def makedirforhash(hash):
	
	filedir = datapath + hash[0:2] + '/' +  hash[2:4] + '/';
	os_makedirs(filedir)
	pass;
#enddef

def filedirfromhash(hash):
	filedir = datapath + hash[0:2] + '/' +  hash[2:4] + '/';
	return filedir;
	pass;
#enddef


r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);
#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);

__all__ = ['redirect', 'response', 'responsefile', 'time', 'json', 'md5', 'encrypt', 'decrypt', 'readfile', 'writefile', 'existfile', 'filesize', 'makedirforhash', 'filedirfromhash', 'r']


