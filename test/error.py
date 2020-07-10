# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


####################################################################
#进行中的任务
task_key_pattern = 'task-*'

task_keys = r.keys(task_key_pattern)

for task_key in task_keys:
	
	task_key = task_key.decode()
	
	state = r.hget(task_key, 'state').decode()
	if state == 'timeout':

		print("timeout task:"+task_key)
		
	#endif
	
#endfor



if __name__ == '__main__':
	pass
#end

