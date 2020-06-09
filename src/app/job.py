# api for vendor

from .init import *

def ping(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		vendor_node_key = 'vendor-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(jsondata['vendor_id'])
		
		vendor_node_ip = request.META['REMOTE_ADDR']
		if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
			vendor_node_ip =  request.META['HTTP_X_FORWARDED_FOR']
		#endif
			
		#set to online
		r.hset(vendor_node_key, 'ping_time', int(time.time()))
		r.hset(vendor_node_key, 'ip', vendor_node_ip)
		
		r.hset(vendor_node_key, 'vendor_id', jsondata['vendor_id'])
		r.hset(vendor_node_key, 'name', jsondata['vendor_name'])
		r.hset(vendor_node_key, 'location', jsondata['vendor_location'])
		r.hset(vendor_node_key, 'state', 'online')
		
		data = 'pong'
		
	else:
		code = 403
		msg = 'method not allowed'	
	#endif
	
	return response(code, msg, data)



def assign(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		job_info = jsondata['job']
				
		#############################
		# make job record
		job_key = 'job-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id'])
		r.hset(job_key, 'state', 'assigned')
		
		# add create timestamp
		r.hset(job_key, 'create_time', int(time.time()))
		r.hset(job_key, 'finish_time', '')
		
		r.hset(job_key, 'vendor_id', jsondata['vendor_id'])
		
		r.hset(job_key, 'worker_group', jsondata['worker_group'])
		r.hset(job_key, 'worker_key', jsondata['worker_key'])
		r.hset(job_key, 'worker_role', jsondata['worker_role'])
		
		r.hset(job_key, 'meta', job_info['meta'])
		r.hset(job_key, 'description', job_info['description'])
		r.hset(job_key, 'priority', job_info['priority'])
		
		
		tasks = jsondata['tasks']
		for task_info in tasks:
			
			#make task records
			if task_info['addressing'] != 'binary':
				task_info['data'] = task_info['data'].encode()
			task_info['hash'] = md5(task_info['data'])
			
			task_key = 'task-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id']) + '-' + task_info['hash']
			r.hset(task_key, 'state', 'assigned')
			r.hset(task_key, 'note', '')
			
			# add create timestamp
			r.hset(task_key, 'create_time', int(time.time()))
			r.hset(task_key, 'start_time', '')
			r.hset(task_key, 'finish_time', '')
			
			
			r.hset(task_key, 'job_id', job_info['job_id'])
			
			r.hset(task_key, 'hash', task_info['hash'])
			
			r.hset(task_key, 'meta', task_info['meta'])
			r.hset(task_key, 'addressing', task_info['addressing'])
			r.hset(task_key, 'port', task_info['port'])
			
			if task_info['addressing'] == 'binary':
				taskdata_filename = filedirfromhash(task_info['hash']) + task_info['hash'] + '.taskdata'
				makedirforhash(task_info['hash'])
				writefile(taskdata_filename, task_info['data'])
				task_info['data'] = ''
			else:
				r.hset(task_key, 'data', task_info['data'])
			#endif
			
			
			#allocate task to work priority list
			work_key = 'work-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['priority'])
			r.lpush(work_key, task_key)
			
			#add task to tasks_waiting to wait for job state check
			tasks_waiting_key = 'tasks_waiting-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']+ '-' + str(job_info['job_id'])
			r.sadd(tasks_waiting_key, task_key)

		#endfor
		
		#update vendor node hit counter
		vendor_node_key = 'vendor-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(jsondata['vendor_id'])
		
		vendor_node_hit = r.hget(vendor_node_key, 'hit')
		if vendor_node_hit == None:
			vendor_node_hit = 1
		else:
			vendor_node_hit = int(vendor_node_hit) + 1
		#endif
		
		r.hset(vendor_node_key, 'hit', vendor_node_hit)
		
	#endif
				
	return response(code, msg, data)

#enddef

def delete(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		job_info = jsondata['job']
		
		#set state to deleted
		job_key = 'job-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id'])
		r.hset(job_key, 'state', 'deleted')
		
		#seek all task in job and delete
		task_key_pattern = 'task-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id']) + "-*"
		task_keys = r.keys(task_key_pattern)
		
		for task_key in task_keys:
			r.hset(task_key, 'state', 'deleted')
			
		#endfor
	#endif	

	return response(code, msg, data)

#enddef
	
def done(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		#seek all jobs done
		jobs_done_key = 'jobs_done-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		job_keys = r.smembers(jobs_done_key)
		job_keys = list(job_keys)
		data['done'] = job_keys

	#endif
	
	return response(code, msg, data)
	
#enddef

def detail(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		job_info = jsondata['job']
		
		job_key = 'job-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id'])
		
		
		data['worker_group'] = r.hget(job_key, 'worker_group').decode()
		data['worker_role'] = r.hget(job_key, 'worker_role').decode()
		

		job_info['meta'] = r.hget(job_key, 'meta').decode()
		job_info['description'] = r.hget(job_key, 'description').decode()
		job_info['priority'] = r.hget(job_key, 'priority').decode()
		job_info['state'] = r.hget(job_key, 'state').decode()
		job_info['create_time'] = r.hget(job_key, 'create_time').decode()
		job_info['finish_time'] = r.hget(job_key, 'finish_time').decode()
		
		data['job'] = job_info
		
		#read result from task
		tasklist = []
		
		task_key_pattern = 'task-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id']) + "-*"
		task_keys = r.keys(task_key_pattern)
		
		for task_key in task_keys:
			task_info = {}
			task_info['meta'] = r.hget(task_key, 'meta').decode()
			task_info['addressing'] = r.hget(task_key, 'addressing').decode()
			task_info['port'] = r.hget(task_key, 'port').decode()
			task_info['state'] = r.hget(task_key, 'state').decode()
			task_info['note'] = r.hget(task_key, 'note').decode()
			task_info['hash'] = r.hget(task_key, 'hash').decode()
			task_info['create_time'] = r.hget(task_key, 'create_time').decode()
			task_info['start_time'] = r.hget(task_key, 'start_time').decode()
			task_info['finish_time'] = r.hget(task_key, 'finish_time').decode()
			
			
			#read result from disk if done
			result = ''
			if task_info['state'] == 'done' or task_info['state'] == 'deleted':
				result_filename = filedirfromhash(task_info['hash']) + task_info['hash'] + '.result'
				if existfile(result_filename) == True:
					result = readfile(result_filename)
				#endif
			
			#endif
			
			task_info['result'] = result
			
			tasklist.append(task_info)
		#endfor
		data['tasks'] = tasklist
		
	#endif
	
	return response(code, msg, data)

#enddef

def mark(request):
	code = 200
	msg = 'ok'
	data = {}

	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		
		job_info = jsondata['job']
		#mark a job as read by remove from set
		jobs_done_key = 'jobs_done-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role']
		job_key = 'job-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['job_id'])
		
		r.srem(jobs_done_key, job_key)
	
	#endif
	
	return response(code, msg, data)

#enddef


if __name__ == '__main__':
	pass
#end



