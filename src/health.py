# api for vendor

from app.init import *

def health_thread(timeout = 300):
	print("started health thread, timeout = %d" % timeout)
	
	while True:
		time.sleep(30)
		vendor_set_all = 'vendor_set_all'
		vendor_keys = list(r.smembers(vendor_set_all))

		vendors = []
		for vendor_key in vendor_keys:
			ping_time = int(r.hget(vendor_key, 'ping_time').decode())
			state = r.hget(vendor_key, 'state').decode()
			if state == 'online':
				if time.time() - ping_time > timeout:
					r.hset(vendor_key, 'state', 'offline')
				#endif
			#endif
			if state == 'offline':
				if time.time() - ping_time < timeout:
					r.hset(vendor_key, 'state', 'online')
				#endif
			#endif
		#endfor
		
		
		worker_set_all = 'worker_set_all'
		worker_keys = list(r.smembers(worker_set_all))

		workers = []
		for worker_key in worker_keys:
			ping_time = int(r.hget(worker_key, 'ping_time').decode())
			state = r.hget(worker_key, 'state').decode()
			if state == 'online':
				if time.time() - ping_time > timeout:
					r.hset(worker_key, 'state', 'offline')
				#endif
			#endif
			if state == 'offline':
				if time.time() - ping_time < timeout:
					r.hset(worker_key, 'state', 'online')
				#endif
			#endif
		#endfor
		
		
		#endfor

	#endwhile
if __name__ == '__main__':
	health_thread()
#end



