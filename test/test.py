# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


a = r.zrank("hello", "2")

b	= r.zrangebyscore("hello", 15, 22)

print(b)


if __name__ == '__main__':
	pass
#end



