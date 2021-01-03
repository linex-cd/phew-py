# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


r.zadd("testset", {"www":211})

x = r.zrank("testset", "www")
print(x)

r.zrem("testset", "www")
x = r.zrank("testset", "www")
print(x)
if __name__ == '__main__':
	pass
#end



