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


def finish_task(session, job, task):
	
	result = None
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['worker_id'] = config.worker_id
	
	data['job'] = job
	data['task'] = task
	
	
	url = 'http://' + config.jobcenter_server + '/task/finish'
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
		log('finish task error')
	
	#endtry
	
	return result
	
#enddef


def main():

	job = {}
	job['job_id'] = 4399
	
	task = {}
	task['hash'] = '4a3af7e431970ad0a3b37c1ae20f1506'
	
	result = {}
	result['state'] = 'done'
	result['ocr'] = 'thisistheresult'
	
	task['result'] = json.dumps(result)

	session = create_session()
	rs = finish_task(session = session, job = job, task = task)
	
	print(rs)
	
#endmain


if __name__ == '__main__':
	main()
#end
	
	
	
	