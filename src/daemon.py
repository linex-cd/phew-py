# api for vendor

from app.init import *

def deamon_thread(timeout = 60):
	log("started deamon thread, timeout = %d" timeout)
	
	#seek all tasks pending
	tasks_pending_key_pattern = 'tasks_pending-*'
	
	tasks_pending_keys = r.keys(tasks_pending_key_pattern)
	
	for tasks_pending_key in tasks_pending_keys:
		
		task_keys = r.smembers(tasks_pending_key)
		task_keys = list(task_keys)
		
		#repush to the right of list if timeout
		for task_key in task_keys:
			task_create_time = r.hget(task_key, 'start_time')
			
			if int(time.time()) - int(task_create_time) > timeout:
				work_key = 'work-' + jsondata['worker_group'] + '-' + jsondata['worker_key'] + '-' + jsondata['worker_role'] + '-' + str(job_info['priority'])
				r.rpush(work_key, task_key)
				
			#endif
			
			#remove from pending set
			r.srem(tasks_pending_key, task_key)
			
		#endfor
	
		
	#endfor

if __name__ == '__main__':
	deamon_thread()
#end



