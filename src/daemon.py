# api for vendor

from app.init import *

def deamon_thread():

	while True:
		time.sleep(10)
		print("seeking all tasks timeout...")
		#seek all tasks pending
		tasks_pending_all = 'tasks_pending_all'
		
		tasks_pending = list(r.smembers(tasks_pending_all))
		
		for task_key in tasks_pending:
			
			task_key = task_key.decode()
						
			#remove from pending set if timeout and mark timeout
		
			try:
				job_id = r.hget(task_key, 'job_id').decode()
				task_create_time = r.hget(task_key, 'start_time')
				task_timeout = r.hget(task_key, 'timeout')
				task_try_times_limit = r.hget(task_key, 'try_times_limit')
				
				tmp = task_key.split("-")
				worker_group = tmp[1]
				worker_key = tmp[2]
				worker_role = tmp[3]
				job_id = tmp[4]
				
				job_key = 'job-' +worker_group + '-'+ worker_key + '-'+ worker_role + '-'+ job_id
				
				tasks_pending_key = 'tasks_waiting-' + worker_group + '-' + worker_key + '-' + worker_role + '-' + job_id
				tasks_waiting_key = tasks_pending_key.replace('tasks_pending-', 'tasks_waiting-')
				
				if int(time.time()) - int(task_create_time) > int(task_timeout):
					
					#try_times under limit
					try_times = int(r.hget(task_key, 'try_times').decode())
					
					if try_times < int(task_try_times_limit):
						print("resend task to work list:%s" % task_key)
			
						#increase try_times
						r.hset(task_key, 'try_times', try_times+1)
						
						#reset state
						r.hset(task_key, 'state','waiting')
						
						#remove from pending set
						r.srem(tasks_pending_key, task_key)
						
						#remove from all pending set
						r.srem(tasks_pending_all, task_key)
						
						#add to waiting set
						r.sadd(tasks_waiting_key, task_key)
						
						#push to work list
						priority = r.hget(task_key, 'priority').decode()
						work_key = 'work-' + worker_group + '-' + worker_key + '-' + worker_role + '-' + str(priority)
						r.rpush(work_key, task_key)
						
						#add to priority set
						priority_set = 'priority_set-' + worker_group + '-' + worker_key + '-' + worker_role
						r.zadd(priority_set, {priority : int(priority) })
										
						

					else:
						print("mark task timeout:%s" % task_key)
						
						#mark state timeout
						r.hset(task_key, 'state', 'timeout')
						
						#remove from  pending set
						r.srem(tasks_pending_key, task_key)
						
						#remove from all pending set
						r.srem(tasks_pending_all, task_key)
						
						#send to error set
						error_job_set_key = 'error_job-' + worker_group + '-' + worker_key + '-' + worker_role
						r.zadd(error_job_set_key, int(time.time()), job_key)
						
						error_task_set_key = 'error_task-' + worker_group + '-' + worker_key + '-' + worker_role
						r.zadd(error_task_set_key, int(time.time()), task_key)
						
						
						#if last one task is timeout, the mark the job as done
						#check if tasks_waiting and tasks_pending set are empty
						if r.scard(tasks_waiting_key) == 0 and r.scard(tasks_pending_key) == 0: 
							#add a job to set as unread
							jobs_done_key = 'jobs_done-' + worker_group + '-' + worker_key + '-' + worker_role

							r.sadd(jobs_done_key, job_id)
							
							#add finish timestamp
							r.hset(job_key, 'finish_time', int(time.time()))
							r.hset(job_key, 'state', 'done')
							
							statistics_job_pending_key = 'statistics_job_pending-' + worker_group + '-' + worker_key + '-' + worker_role
							r.decr(statistics_job_pending_key, 1)
							
							if int(r.get(statistics_job_pending_key).decode()) < 0:
								r.set(statistics_job_pending_key, 0)
							#endif
							
						#endif
					#endif
					
					
				#endif
			except:
				print('some key dismissed, continue')
				continue
			#endtry
			
		

		#endfor
		
	#endwhile
if __name__ == '__main__':
	deamon_thread()
#end



