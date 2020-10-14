# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


####################################################################

#出错的task
error_task_keys_pattern = 'error_task-*'

error_task_keys = r.keys(error_task_keys_pattern)

for error_task_key in error_task_keys:
	
	error_task_key = error_task_key.decode()
	
	error_tasks = list(r.smembers(error_task_key));
	print("error_tasks len:"+str(len(error_tasks)))
	for task_key in error_tasks:
	
		task_key = task_key.decode()
		
		job_key = 
		state = r.hget(job_key, 'state').decode()
		
		print(job_key+":"+state)
		if state == 'deleted':
			
			print("cleaning job_key:"+job_key)
			
			#seek all task in job and delete
			task_key_pattern = job_key.replace("job-", "task-") + "-*"
			task_keys = r.keys(task_key_pattern)
			
			for task_key in task_keys:

				task_key = task_key.decode()
				
				#delete task excluding from error list
				error_task_set_key = job_key.replace("job-", "error_task-")
				error_task_set_key = error_task_set_key[:error_task_set_key.rfind("-")]
				
				r.delete(task_key)
				r.srem(error_task_set_key, task_key)

				print("remove from "+error_task_set_key+" task:"+task_key)
			#endfor

			
		#endif
		
	#endfor
#endfor




if __name__ == '__main__':
	pass
#end

