# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


task_keys_pattern = 'task-*'

task_keys = r.keys(task_keys_pattern)

data = {}

for task_key in task_keys:
	
	task_key = task_key.decode()
	
	s = r.hget(task_key, 'start_time').decode()
	f = r.hget(task_key, 'finish_time').decode()
	if f == '':
		continue
	d = int(f)-int(s)
	if str(d) in data:
		data[str(d)] = data[str(d)] + 1
	else:
		data[str(d)] = 1

f = open("sts.txt", "w")
for k in data:
	line = k + ',' + str(data[k]) + '\n'
	f.write(line)
	
f.close()


	

if __name__ == '__main__':
	pass
#end



