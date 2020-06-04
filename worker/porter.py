
import traceback
import json
import requests
import os
import sys

import time


import cv2
import numpy as np


import config
from utils import *

#冷加载可用模块
port_dir = "port"
sys.path.append(port_dir)

module_list = []
init_str = ""
fileList = os.listdir(port_dir)

for file_name in fileList:
	if file_name == "__init__.py":
		continue			
	#endif
			
	if file_name[-3:] != ".py":
		continue			
	#endif
	
	module_name = file_name[0:-3]
	
	#try:
	if 1:
		init_str += "from "+port_dir+" import "+module_name+"\n"
		exec(init_str,globals())
		module_list.append(module_name)
		log('Loading module succeeded: %s' % module_name)
	#except:
	else:
		log("Loading module failed: %s" % module_name)
	#endtry
	
	
#endfor

log('All modules loaded')

def port_task(task):

	note = ''
	result = None
	# {'job_id': '4399', 'addressing': 'URL', 'port': 'ocr', 'hash': '5b3e5b887619c1bd2df53a6c62498914', 'data': 'http://127.0.0.1:2020/1.jpg'}
	
	file_name = ''
	port = task['port']
	
	###################################################################
	#判断端口是否存在
	if port not in module_list:
		note = 'port not installed'
		return note, result
	#endif
	
	###################################################################
	#判断数据类型
	
	
	addressing = task['addressing']
	if addressing == 'URL':
		file_name = task['hash']
		url = task['data']
		
		#下载文件,最长等待10分钟
		response = None
		try:
			response = requests.get(url = url, timeout = 60*10)
		except:
			note = 'download file timeout'
			return note, result
		#endtry
		
		
		if response.status_code != 200:
			note = 'download file error, code:%d' % response.status_code
			return note, result
		#endif
		
		chunk_size = 1024
		with open(file_name, "wb") as file:
			for data in response.iter_content(chunk_size = chunk_size):
				file.write(data)
			#endfor
		#endwhile
		
	elif addressing == 'URI':
		file_name = task['data']
		
	else:
		pass
		
	#endif
	
	###################################################################
	#根据任务端口尝试加载模块
	

	exe_str = port+'.run("'+file_name+'")'	
	result = eval(exe_str, globals())

	#移除临时文件
	if addressing == 'URL':
		try:
			os.remove(file_name)
		except:
			pass
		#endtry
	#endif

	return note, result
#enddef

if __name__ == "__main__":
	pass
#enddef
