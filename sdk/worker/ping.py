import json;
import requests;

import config;

import traceback;

def log(msg):

	print(msg)
	
#enddef


def create_session():

	return requests.session();
#enddef


def ping(session):
	
	task = None
	
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
		print(resp.text)
		ret = json.loads(resp.text)
		
		log(str(ret['code']) +  ":"  +  ret['msg'])
		if ret['code'] == 200:
			task = ret['data']

		#endif
	except:
		traceback.print_exc()
		log('get task error')
	
	#endtry
	
	return task
	
#enddef

def main():


	session = create_session()
	rs = ping(session = session)
	
	print(rs)
	
#endmain


if __name__ == '__main__':
	main()
#end
	
	
	
	