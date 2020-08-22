# api for vendor

from app.init import *

def deamon_thread(timeout = 60):
	print("started deamon thread, timeout = %d" % timeout)
	
	while True:
		time.sleep(30)
		print("seeking all tasks timeout...")
		#seek all tasks pending
		tasks_pending_key_pattern = 'tasks_pending-*'
		
		tasks_pending_keys = r.keys(tasks_pending_key_pattern)
		
		for tasks_pending_key in tasks_pending_keys:
			
			tasks_pending_key = tasks_pending_key.decode()
			
			tmp = tasks_pending_key.split('-')
			worker_group = tmp[1]
			worker_key = tmp[2]
			worker_role = tmp[3]
			
			task_keys = r.smembers(tasks_pending_key)
			task_keys = list(task_keys)
			
			#remove from pending set if timeout and mark timeout
			for task_key in task_keys:
				task_key = task_key.decode()
				try:
					job_id = r.hget(task_key, 'job_id').decode()
					task_create_time = r.hget(task_key, 'start_time')
					
					if int(time.time()) - int(task_create_time) > timeout:
						
						print("mark task timeout:%s" % task_key)
						
						r.hset(task_key, 'state', 'timeout')
						r.srem(tasks_pending_key, task_key)
						
						tasks_waiting_key = tasks_pending_key.replace('tasks_pending-', 'tasks_waiting-')
						r.srem(tasks_waiting_key, task_key)
						
						#send to error list
						
						job_key = 'job-' + worker_group + '-' + worker_key + '-' + worker_role + '-' + job_id
						
						error_job_set_key = 'error_job-' + worker_group + '-' + worker_key + '-' + worker_role
						r.sadd(error_job_set_key, job_key)
						
						error_task_set_key = 'error_task-' + worker_group + '-' + worker_key + '-' + worker_role
						r.sadd(error_task_set_key, task_key)
						
						
						#if last one task is timeout, the mark the job as done
						#check if tasks_waiting and tasks_pending set are empty
						if r.scard(tasks_waiting_key) == 0 and r.scard(tasks_pending_key) == 0: 
							#add a job to set as unread
							jobs_done_key = 'jobs_done-' + worker_group + '-' + worker_key + '-' + worker_role

							r.sadd(jobs_done_key, job_id)
							
							#add finish timestamp
							r.hset(job_key, 'finish_time', int(time.time()))
							r.hset(job_key, 'state', 'done')
						#endif
						
					#endif
				except:
					print('some key dismissed, continue')
					continue
				#endtry
				
			#endfor

		#endfor
		
	#endwhile
if __name__ == '__main__':
	deamon_thread()
#end



