# api for vendor

from app.init import *

def deamon_thread(timeout = 60):
	print("started deamon thread, timeout = %d" % timeout)
	
	while True:
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
					
					job_id = r.hget(task_key, 'job_id')
					priority = r.hget(task_key, 'priority')
					
					#task-Nanjing-testkey12345-textise-528-00cc0111177002930684f5aeef5d4181
					tmp = task_key.split("-")
					worker_group = tmp[1]
					worker_key = tmp[2]
					worker_role = tmp[3]
					
					work_key = 'work-' + worker_group + '-' + worker_key + '-' + worker_role + '-' + str(priority)
					r.rpush(work_key, task_key)
					
				#endif
				
				#remove from pending set
				r.srem(tasks_pending_key, task_key)
				
			#endfor

		#endfor
		time.sleep(30)
	#endwhile
if __name__ == '__main__':
	deamon_thread()
#end



