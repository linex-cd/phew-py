# api for textise

from .init import *

def ping(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		worker_node_key = 'worker_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_' + str(jsondata['worker_id'])
		
		worker_node_ip = request.META['REMOTE_ADDR']
		if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
			worker_node_ip =  request.META['HTTP_X_FORWARDED_FOR']
		#endif
			
		#set to online
		r.hset(worker_node_key, 'ping_time', int(time.time()))
		r.hset(worker_node_key, 'ip', worker_node_ip)
		
		r.hset(worker_node_key, 'worker_id', jsondata['worker_id'])
		r.hset(worker_node_key, 'name', jsondata['worker_name'])
		r.hset(worker_node_key, 'location', jsondata['worker_location'])
		r.hset(worker_node_key, 'state', 'online')
		
		data = 'pong'
		
	else:
		code = 403
		msg = 'method not allowed'	
	#endif
	
	return response(code, msg, data)

#enddef

def get(request):
	code = 200
	msg = 'ok'
	data = {}
	
	if request.method == 'POST':
		
		jsondata = json.loads(request.body.decode())
		
		#update worker node ping state
		worker_node_key = 'worker_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_' + str(jsondata['worker_id'])
		
		worker_node_hit = r.hget(worker_node_key, 'hit')
		if worker_node_hit == None:
			worker_node_hit = 1
		else:
			worker_node_hit = int(worker_node_hit) + 1
		#endif

		r.hset(worker_node_key, 'hit', worker_node_hit)
		
		#############################
		#get all work list keys
		work_key_pattern = 'work_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_*'
		work_keys = r.keys(work_key_pattern)
		
		if len(work_keys) == 0:
			code = 404
			msg = 'no task'
			return response(code, msg, data)
		#endif
		
		#sort and get the highest priority key
		work_keys = sorted(work_keys, reverse=True)
		work_key = work_keys[0]
		
		#popup a valid task_key and get the task info
		task_info = {}
		while True:
			task_key = r.rpop(work_key)
			if task_key == None:
				code = 404
				msg = 'no task'
				break
			#endif
			
			task_info['job_id'] = r.hget(task_key, 'job_id').decode()
			task_info['addressing'] = r.hget(task_key, 'addressing').decode()
			task_info['port'] = r.hget(task_key, 'port').decode()
			task_info['hash'] = r.hget(task_key, 'hash').decode()
						
			#read data from disk if done
			if task_info['addressing'] == 'binary':
				taskdata_filename = filedirfromhash(task_info['hash']) + task_info['hash'] + '.taskdata'
				if existfile(taskdata) == True:
					taskdata = readfile(taskdata_filename)
					task_info['data'] = r.hget(task_key, 'data').decode()
					r.hset(task_key, 'state', 'pending')
					break
				else:
					#mark task as error and then repop a new task
					r.hset(task_key, 'state', 'error')
					continue
				#endif
			else:
				task_info['data'] = r.hget(task_key, 'data').decode()
				r.hset(task_key, 'state', 'pending')
				break
			#endif
			
		#endwhile
		
		data = task_info
			
	else:
		code = 403
		msg = 'method not allowed'	
	#endif
	return response(code, msg, data)
#enddef

def finish(request):
	code = 200
	msg = 'ok'
	data = {}
	
	if request.method == 'POST':
		
		jsondata = json.loads(request.body.decode())
		
		#update worker node ping state
		worker_node_key = 'worker_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_' + str(jsondata['worker_id'])
		
		worker_node_hit = r.hget(worker_node_key, 'hit')
		if worker_node_hit == None:
			worker_node_hit = 1
		else:
			worker_node_hit = int(worker_node_hit) + 1
		#endif
		
		#############################
		#update task result and state
		task_info = jsondata['task']
		
		job_key = 'job_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_' + str(task_info['job_id'])
		
		task_key = 'task_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role'] + '_' + str(task_info['job_id']) + '_' + task_info['hash']
		
		old_task_state = r.hset(task_key, 'state')
		if old_task_state != None:
			old_task_state = old_task_state.decode()
			
			#keep deleted state
			if old_task_state == 'deleted':
				task_info['state'] = old_task_state
			#endif
		#endif
			
		r.hset(task_key, 'state', task_info['state'])
		r.hset(task_key, 'result', task_info['result'])
		
		#remove from tasks_pending set 
		tasks_pending_key = 'tasks_pending_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role']+ '_' + str(task_info['job_id'])
		r.srem(tasks_pending_key, task_key)
		
		#check if tasks_pending set is empty
		if r.scard(tasks_pending_key) == 0: 
			#add a job to set as unread
			jobs_done_key = 'jobs_done_' + jsondata['worker_group'] + '_' + jsondata['worker_key'] + '_' + jsondata['worker_role']

			r.sadd(jobs_done_key, job_key)
		#endif
		
	else:
		code = 403
		msg = 'method not allowed'
	#endif	
	
	return response(code, msg, data)


#enddef

if __name__ == '__main__':
	pass
#end



