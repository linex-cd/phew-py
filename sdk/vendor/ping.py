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
		
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['vendor_id'] = config.vendor_id
	data['vendor_name'] = config.vendor_name
		
	data['vendor_location'] = config.vendor_location

	url = 'http://' + config.jobcenter_server + '/job/ping'
	timeout = 30
	
	try:
		resp = session.post(url = url, data = json.dumps(data), timeout = timeout);

		ret = json.loads(resp.text)
		
		log(str(ret['code']) +  ":"  +  ret['msg'])
		if ret['code'] == 200:
			return True
		#endif
	except:
		traceback.print_exc()
		log('ping error')
	
	#endtry
	
	return False
	
#enddef

def main():


	session = create_session()
	rs = ping(session = session)
	
	print(rs)
	
#endmain


if __name__ == '__main__':
	main()
#end
	
	
	
	