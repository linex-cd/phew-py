# api for vendor
import redis

#r = redis.Redis(host = '192.168.2.29', port = 2019, db = 0);
r = redis.Redis(host = '127.0.0.1', port = 2019, db = 0);


p = r.pipeline()

k = "kkk"
p.incr(k,1)
p.incr(k,1)

print(int(r.get(k).decode()))

p.execute()

print(int(r.get(k).decode()))


if __name__ == '__main__':
	pass
#end



