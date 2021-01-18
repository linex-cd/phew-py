# api for textise

from .init import *

def ping(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		worker_node_key = 'worker-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(jsondata['worker_id'])
		
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
		
		#add to worker set
		worker_set = 'worker_set-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		r.sadd(worker_set, worker_node_key)
		
		#add to worker all set
		worker_set_all = 'worker_set_all'
		r.sadd(worker_set_all, worker_node_key)
		
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
		
		
		#############################
		#get priority list
		priority_set = 'priority_set-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		prioritys = r.zrevrange(priority_set, 0, -1)
		
		if len(prioritys) == 0:
		
			code = 404
			msg = 'no task'
			return response(code, msg, data)
		#endif
		
		#get the highest priority key
		priority =  prioritys[0].decode()
		work_key = 'work-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(priority)
		
		#popup a valid task_key and get the task info
		task_info = None
		while True:
			task_key = r.rpop(work_key)
			if task_key == None:
			
				#remove priority from priority set
				r.zrem(priority_set, priority)
			

				code = 404
				msg = 'no task'
				return response(code, msg, data)
			#endif
			
			job_id = r.hget(task_key, 'job_id')
			if job_id is None:
				continue
			#endif
			
			task_info = {}
			
			task_info['job_id'] = job_id.decode()
			task_info['priority'] = r.hget(task_key, 'priority').decode()
			task_info['meta'] = r.hget(task_key, 'meta').decode()
			task_info['addressing'] = r.hget(task_key, 'addressing').decode()
			task_info['port'] = r.hget(task_key, 'port').decode()
			task_info['hash'] = r.hget(task_key, 'hash').decode()
			task_info['index'] = r.hget(task_key, 'index').decode()
			
			# add start timestamp
			r.hset(task_key, 'start_time', int(time.time()))
				
			#read data from disk if done
			if task_info['addressing'] == 'binary':
				taskdata_filename = filedirfromhash(task_info['hash']) + task_info['hash'] + '.taskdata'
				if existfile(taskdata_filename) == True:
					taskdata = readfile(taskdata_filename)
					task_info['data'] = taskdata
					r.hset(task_key, 'state', 'waiting')
					break
				else:
					#mark task as error and then repop a new task
					r.hset(task_key, 'state', 'error')
					
					# add finish timestamp
					r.hset(task_key, 'finish_time', int(time.time()))
			
					continue
				#endif
			else:
				task_info['data'] = r.hget(task_key, 'data').decode()
				r.hset(task_key, 'state', 'waiting')
				
				break
			#endif
			
		#endwhile
		
		data = task_info
		
		#add to tasks_pending
		tasks_pending_key = 'tasks_pending-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(task_info['job_id'])
		r.sadd(tasks_pending_key, task_key)
		
		#add to tasks_pending total set
		tasks_pending_set = 'tasks_pending_set-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		r.sadd(tasks_pending_set, task_key)
		
		#add to tasks_pending all set
		tasks_pending_all = 'tasks_pending_all'
		r.sadd(tasks_pending_all, task_key)
		
		#remove from tasks_waiting set 
		tasks_waiting_key = 'tasks_waiting-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']+ '-' + str(task_info['job_id'])
		r.srem(tasks_waiting_key, task_key)
		
		#update worker node hit counter
		worker_node_key = 'worker-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(jsondata['worker_id'])
		
		worker_node_hit = r.hget(worker_node_key, 'hit')
		if worker_node_hit == None:
			worker_node_hit = 1
		else:
			worker_node_hit = int(worker_node_hit) + 1
		#endif

		r.hset(worker_node_key, 'hit', worker_node_hit)
		
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
				
		#############################
		#update task result and state
		task_info = jsondata['task']
		
		job_key = 'job-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(task_info['job_id'])
		
		task_key = 'task-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(task_info['job_id']) + '-' + task_info['index']
		
		old_task_state = r.hget(task_key, 'state')
		if old_task_state != None:
			old_task_state = old_task_state.decode()
			
			#keep deleted state
			if old_task_state == 'deleted':
				task_info['state'] = old_task_state
			#endif
		else:
			#already deleted
			return response(code, msg, data)
		#endif
		
		# add finish timestamp
		r.hset(task_key, 'finish_time', int(time.time()))
		
		r.hset(task_key, 'state', task_info['state'])
		r.hset(task_key, 'note', task_info['note'])
		r.hset(task_key, 'result', task_info['result'])
		
		#remove from tasks_pending
		tasks_pending_key = 'tasks_pending-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']+ '-' + str(task_info['job_id'])
		r.srem(tasks_pending_key, task_key)
		
		#remove from tasks_pending total set
		tasks_pending_set = 'tasks_pending_set-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		r.srem(tasks_pending_set, task_key)
		
		#remove from tasks_pending all set
		tasks_pending_all = 'tasks_pending_all'
		r.srem(tasks_pending_all, task_key)
		
		tasks_waiting_key = 'tasks_waiting-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']+ '-' + str(task_info['job_id'])
		
		#delete binary tmp file
		if task_info['addressing'] == 'binary':
			taskdata_filename = filedirfromhash(task_info['hash']) + task_info['hash'] + '.taskdata'
			if existfile(taskdata_filename) == True:
				removefile(taskdata_filename)
			#endif
		#endif
		
		#check if tasks_waiting and tasks_pending set are empty
		if r.scard(tasks_waiting_key) == 0 and r.scard(tasks_pending_key) == 0: 
			#add a job to set as unread
			jobs_done_key = 'jobs_done-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']

			r.sadd(jobs_done_key, task_info['job_id'])
			
			#add finish timestamp
			r.hset(job_key, 'finish_time', int(time.time()))
			r.hset(job_key, 'state', 'done')
			
			#job pending statistics
			statistics_job_pending_key = 'statistics_job_pending-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] 
			r.decr(statistics_job_pending_key, 1)
			
			if int(r.get(statistics_job_pending_key).decode()) < 0:
				r.set(statistics_job_pending_key, 0)
			#endif
			
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



