# api for vendor
import redis
import time

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


task_keys_pattern = 'job-*'

task_keys = r.keys(task_keys_pattern)

f = open("check.txt", "w")

c1 = 1592305200
f1 = 1592312400

for task_key in task_keys:
	
	task_key = task_key.decode()
	
	c0 = r.hget(task_key, 'create_time').decode()
	f0 = r.hget(task_key, 'finish_time').decode()
	if f0 == '':
		continue
		
	if int(c0) < c1:
		continue
		
	if int(f0) > f1:
		continue
	c2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(c0)));
	f2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(f0)));
	line = c2+','+f2+"\n"
	f.write(line)
	
f.close()


	

if __name__ == '__main__':
	pass
#end



