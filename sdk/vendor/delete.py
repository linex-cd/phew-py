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


def delete_job(session, job):
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['vendor_id'] = config.vendor_id
	

	data['job'] = job

	url = 'http://' + config.jobcenter_server + '/job/delete'
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
		log('delete job error')
	
	#endtry
	
	return False
	
#enddef


def main():

	job_id = 4399
	
	job_info = {}
	job_info['job_id'] = str(job_id)

	
	session = create_session()
	rs = delete_job(session = session, job = job_info)
	
	print(rs)
	
#endmain

if __name__ == '__main__':
	main()
#end

	
	
	
	