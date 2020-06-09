import json;
import requests;

import traceback;

import config;

def log(msg):

	print(msg)
	
#enddef


def create_session():

	return requests.session();
#enddef


def done_job(session):
	result = None
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['vendor_id'] = config.vendor_id
	

	url = 'http://' + config.jobcenter_server + '/job/done'
	timeout = 30
	
	try:
		resp = session.post(url = url, data = json.dumps(data), timeout = timeout);

		ret = json.loads(resp.text)
		
		log(str(ret['code']) +  ":"  +  ret['msg'])
		if ret['code'] == 200:
			return ret['data']
		#endif
	except:
		traceback.print_exc()
		log('done job error')
	
	#endtry
	
	return result
	
#enddef


def main():

	session = create_session()
	rs = done_job(session = session)
	
	print(rs)
	
#endmain

if __name__ == '__main__':
	main()
#end

	
	
	
	