import json;
import requests;
import time;


import traceback;

import config;
from utils import *;


def create_session():

	return requests.session();
#enddef


def ping(session):
	
	result = None
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['worker_id'] = config.worker_id
	data['worker_name'] = config.worker_name
		
	data['worker_location'] = config.worker_location

	url = 'http://' + config.jobcenter_server + '/task/ping'
	timeout = 30
	
	try:
		resp = session.post(url = url, data = json.dumps(data), timeout = timeout);

		ret = json.loads(resp.text)
		
		log(str(ret['code']) +  ":"  +  ret['msg'])
		if ret['code'] == 200:
			result = ret['data']

		#endif
	except:
		traceback.print_exc()
		log('ping error')
	
	#endtry
	
	return result
	
#enddef

def ping_thread():


	MAX_TRY_TIMES = 100
	CUR_TRY_TIMES = 0
	
	session = create_session()
	
	while True:
		time.sleep(30)
		try:
			#检测服务器
			result = ping(session)
			
			if result != None:
				#归零失败计数器
				CUR_TRY_TIMES = 0
				continue

			else:
				CUR_TRY_TIMES = CUR_TRY_TIMES + 1
				if CUR_TRY_TIMES>=MAX_TRY_TIMES:
					log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
					return
				else:
					session = create_session()
					continue
				#endif
			#endif
			
			
	
		except:
			traceback.print_exc()
			
			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				return
			else:
				session = create_session()
				continue
			#endif

		#endtry
		
		
	#endwhile
#enddef


if __name__ == '__main__':
	pass;
#end
	
	
	
	