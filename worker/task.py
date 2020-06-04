import json;
import requests;
import time;

import config;

import traceback;


from porter import port_task;


from utils import *;

def create_session():

	return requests.session();
#enddef


def get_task(session):
	
	task = None
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['worker_id'] = config.worker_id
	
	url = 'http://' + config.jobcenter_server + '/task/get'
	timeout = 30
	
	try:
		resp = session.post(url = url, data = json.dumps(data), timeout = timeout);

		ret = json.loads(resp.text)
		
		log(str(ret['code']) +  ":"  +  ret['msg'])
		if ret['code'] == 200:
			task = ret['data']
		#endif
		if ret['code'] == 404:
			task = ''
		#endif
	except:
		traceback.print_exc()
		log('get task error')
	
	#endtry
	
	return task
	
#enddef



def finish_task(session, task):
	
	data = {}
	
	data['worker_group'] = config.worker_group
	data['worker_key'] = config.worker_key
	data['worker_role'] = config.worker_role
	
	data['worker_id'] = config.worker_id
	
	data['task'] = task
	
	
	url = 'http://' + config.jobcenter_server + '/task/finish'
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
		log('finish task error')
	
	#endtry
	
	return False
	
#enddef


def task_thread():


	MAX_TRY_TIMES = 100
	CUR_TRY_TIMES = 0
	
	session = create_session()
	
	while True:
		time.sleep(1)
		
		#拉取任务
		task = None
		
		task = get_task(session)
		
		if task != None:
			
			if task == '':
				log('暂时没有任务')
				time.sleep(10)
				continue
				
			#endif
			
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
		

		
		
		#根据任务类型分配port
		note = ''
		result = ''
		state = 'error'
		try:
			note, result = port_task(task)
			if result != None:
				state = 'done'
			#endif		
			
		except:
			log('操作任务失败')
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
		
		
		#上传任务结果

		task['state'] = state
		task['note'] = note
		
		if type(result) == dict or type(result) == list or type(result) == tuple:
			result = json.dumps(result)
		#endif
		task['result'] = result

		ret = finish_task(session, task)
		

		if ret == True:
			#归零失败计数器
			CUR_TRY_TIMES = 0
		else:
			log('上传任务结果失败')
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
		
		log('操作任务成功')
		
	#endwhile
#enddef

if __name__ == '__main__':
	pass
#endif