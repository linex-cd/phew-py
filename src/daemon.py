# api for vendor

from app.init import *

def deamon_thread(timeout = 60):
	print("started deamon thread, timeout = %d" % timeout)
	
	while True:
		print("seeking all tasks timeout...")
		#seek all tasks pending
		tasks_pending_key_pattern = 'tasks_pending-*'
		
		tasks_pending_keys = r.keys(tasks_pending_key_pattern)
		
		for tasks_pending_key in tasks_pending_keys:
			
			task_keys = r.smembers(tasks_pending_key)
			task_keys = list(task_keys)
			
			#remove from pending set if timeout and mark timeout
			for task_key in task_keys:
			
				job_id = r.hget(task_key, 'job_id')
				task_create_time = r.hget(task_key, 'start_time')
				
				if int(time.time()) - int(task_create_time) > timeout:
					
					print("mark task timeout:%s" % task_key.decode())
					
					r.hset(task_key, 'state', 'timeout')
					r.srem(tasks_pending_key, task_key)
					
					tasks_waiting_key = tasks_pending_key.decode().replace('tasks_pending-', 'tasks_waiting-')
					r.srem(tasks_waiting_key, task_key)
					
					#if last one task is timeout, the mark the job as done
					#check if tasks_waiting and tasks_pending set are empty
					if r.scard(tasks_waiting_key) == 0 and r.scard(tasks_pending_key) == 0: 
						#add a job to set as unread
						
						tmp = tasks_waiting_key.split('-')
						worker_group = tmp[1]
						worker_key = tmp[2]
						worker_role = tmp[3]
						
						job_key = 'job-' + worker_group + '-' + worker_key + '-' + worker_role+ '-' + str(job_id)
		
						jobs_done_key = 'jobs_done-' + worker_group + '-' + worker_key + '-' + worker_role

						r.sadd(jobs_done_key, job_id)
						
						#add finish timestamp
						r.hset(job_key, 'finish_time', int(time.time()))
						r.hset(job_key, 'state', 'done')
					#endif
					
				#endif

				
			#endfor

		#endfor
		time.sleep(30)
	#endwhile
if __name__ == '__main__':
	deamon_thread()
#end



