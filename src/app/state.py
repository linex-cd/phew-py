# api for monitor

from .init import *

import psutil

import pynvml
pynvml.nvmlInit()


def index(request):
	return redirect("/index.html")

def sysstate(request):
	

	if request.method == 'GET':
		
		#REDIS DB  4G
		db = int(filesize('/jobcenterdata/redis.rdb') / (1024*1024*1024*4) * 100)

		
		#CPU
		cpu = int(psutil.cpu_percent())
		
		#memory
		memory =  int(psutil.virtual_memory().percent)
		
		#disk
		disk = int(psutil.disk_usage("/").percent)

		#GPU
		# 这里的0是GPU id
		gpuhandle = pynvml.nvmlDeviceGetHandleByIndex(0)
		gpuinfo = pynvml.nvmlDeviceGetMemoryInfo(gpuhandle)
		gpu = int(gpuinfo.used / gpuinfo.total * 100)
		
		#network MB
		before = psutil.net_io_counters().bytes_recv
		time.sleep(0.1)
		now = psutil.net_io_counters().bytes_recv
		network = int((now-before)*10 /1024/1024)
		
		#temp
		temp = 0
		if hasattr(psutil, 'sensors_temperatures'):
			temp = int(psutil.sensors_temperatures()['coretemp'][0].current)
		#endif
			
		data  = {
					'db': db,
					'cpu': cpu,
					'memory': memory,
					'gpu': gpu,
					'disk': disk,
					'network': network,
					'temp': temp,
				}
		

	return response(200, "ok", data)

def jobcounter(request):
	

	if request.method == 'GET':
		
		job_total_pattern = 'job-*'
		jobs = r.keys(job_total_pattern)
		job_total = len(jobs)
		
		
		job_pending = 0
		task_total = 0
		
		job_latest = []
		for job in jobs:
		
			job_key = job.decode()
			
			#job_pending
			state = r.hget(job_key, 'state').decode()
			if state == 'assigned':
				job_pending = job_pending + 1
			#endif
			
			#task_total
			length = int(r.hget(job_key, 'length').decode())
			task_total = task_total + length
			
			#latest
			description = r.hget(job_key, 'description').decode()
			job_id = job_key.split("-")[-1]
			create_time = r.hget(job_key, 'create_time').decode()
			item = (create_time, length, job_id, description)
			job_latest.append(item)
			
		#endfor
		
		work_pattern = 'work-*'
		task_pending = len(r.keys(work_pattern))
		
		#job_latest sort by create_time
		job_latest = sorted(job_latest, key=lambda x: (x[0]))
		
		#task_latest
		task_latest = []
		tasks_pending_pattern = 'tasks_pending-*'
		tasks = r.keys(tasks_pending_pattern)
		for task in tasks:
			job_key = 'job-' + task.decode()[5:-33]
			item = {}
			item['job_id'] = job_key.split("-")[-1]
			item['description'] =  r.hget(job_key, 'description').decode()
			
			item['port'] =  r.hget(task, 'port').decode()
			item['data'] =  r.hget(job_key, 'data').decode()
			
			task_latest.append(item)
		#endfor
		
		
		
		data  = {
					'job_total': job_total,
					'task_total': task_total,
					'job_pending': job_pending,
					'task_pending': task_pending,
					'job_latest': job_latest,
					'task_latest': task_latest,
				}
		

	return response(200, "ok", data)



def nodecounter(request):
	

	if request.method == 'GET':
		
		vendor_pattern = 'vendor-*'
		vendor_keys = r.keys(vendor_pattern)
		vendor_count = len(vendor_keys)
		vendors = []
		for vendor_key in vendor_keys:
			item = {}
			itemkeys = r.hgetall(vendor_key)
			for itemkey in itemkeys:
				item[itemkey.decode()] = r.hget(vendor_key, itemkey).decode()
			#endfor
			vendors.append(item)
		#endfor
		
		
		worker_pattern = 'worker-*'
		worker_keys = r.keys(worker_pattern)
		worker_count = len(worker_keys)
		workers = []
		for worker_key in worker_keys:
			item = {}
			itemkeys = r.hgetall(worker_key)
			for itemkey in itemkeys:
				item[itemkey.decode()] = r.hget(worker_key, itemkey).decode()
			#endfor
			workers.append(item)
		#endfor
		
		
		data  = {
					'vendor_count': vendor_count,
					'worker_count': worker_count,
					'vendors': vendors,
					'workers': workers,
				}
		

	return response(200, "ok", data)





