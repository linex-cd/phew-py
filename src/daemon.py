# api for vendor

from app.init import *

def deamon_thread(timeout = 60):
	print("started deamon thread, timeout = %d" % timeout)
	
	while True:
		print("seeking all tasks pending...")
		#seek all tasks pending
		tasks_pending_key_pattern = 'tasks_pending-*'
		
		tasks_pending_keys = r.keys(tasks_pending_key_pattern)
		
		for tasks_pending_key in tasks_pending_keys:
			
			task_keys = r.smembers(tasks_pending_key)
			task_keys = list(task_keys)
			
			#remove from pending set if timeout and mark timeout
			for task_key in task_keys:
				task_create_time = r.hget(task_key, 'start_time')
				
				if int(time.time()) - int(task_create_time) > timeout:			
					r.hget(task_key, 'state', 'timeout')
					r.srem(tasks_pending_key, task_key)					
					
				#endif

				
			#endfor

		#endfor
		time.sleep(30)
	#endwhile
if __name__ == '__main__':
	deamon_thread()
#end



