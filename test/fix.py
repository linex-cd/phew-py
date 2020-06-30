# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


job_key_pattern = 'job-Nanjing-testkey12345-textise-*'

job_keys = r.keys(job_key_pattern)

for job_key in job_keys:
	
	job_key = job_key.decode()
	
	l = r.hget(job_key, 'length')
	if l == None:

		task_key_pattern = job_key.replace('job','task')+ '-*'
		task_keys = r.keys(task_key_pattern)
		
		length = len(task_keys)
		
		r.hset(job_key, 'length', length)
		
		print(job_key)
		print(length)
	#endif
	

if __name__ == '__main__':
	pass
#end



