# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


key_pattern = 'task-*'

keys = r.keys(key_pattern)

for key in keys:
	
	key = key.decode()
	
	data = r.hget(key, 'create_time')
	if data == None:


		r.hdel(key, 'finish_time')
		r.hdel(key, 'result')
		r.hdel(key, 'note')
		r.hdel(key, 'state')

		
		print(key)
		
	#endif
	

if __name__ == '__main__':
	pass
#end



