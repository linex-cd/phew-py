# api for monitor

from .init import *

import psutil


import pynvml
gpustate = 0
try:
	pynvml.nvmlInit()
	gpustate = 1
except:
	print("can not init nvidia driver")
#endtry

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
		
		#systemdisk
		systemdisk = int(psutil.disk_usage("/").percent)
		
		#datadisk
		datadisk = int(psutil.disk_usage("/jobcenterdata/").percent)

		#GPU
		gpu = 90
		if gpustate == 1:
			# 这里的0是GPU id
			gpuhandle = pynvml.nvmlDeviceGetHandleByIndex(0)
			gpuinfo = pynvml.nvmlDeviceGetMemoryInfo(gpuhandle)
			gpu = int(gpuinfo.used / gpuinfo.total * 100)

		#endif
		
		#temp
		temp = 0
		if hasattr(psutil, 'sensors_temperatures'):
			tempdata = psutil.sensors_temperatures()
			if 'coretemp' in tempdata:
				temp = int(tempdata['coretemp'][0].current)
			#endif
		#endif
			
		data  = {
					'db': db,
					'cpu': cpu,
					'memory': memory,
					'gpu': gpu,
					'systemdisk': systemdisk,
					'datadisk': datadisk,
					'temp': temp,
				}
		

	return response(200, "ok", data)

def latestwork(request):
	if request.method == 'GET':
		
		job_total_pattern = 'job-*'
		jobs = r.keys(job_total_pattern)

		job_latest = []
		for job in jobs:
		
			job_key = job.decode()
			
			#latest
			length = int(r.hget(job_key, 'length').decode())
			description = r.hget(job_key, 'description').decode()
			job_id = job_key.split("-")[-1]
			create_time = r.hget(job_key, 'create_time').decode()
			item = (create_time, length, job_id, description, encrypt(job_key))
			job_latest.append(item)
			
		#endfor
		
		#job_latest sort by create_time
		job_latest = sorted(job_latest, key=lambda x: (x[0]))
		job_latest = job_latest[-20:]

	
		#task_latest
		task_latest = []
		tasks_pending_pattern = 'tasks_pending-*'
		tasks_pending_set_keys = r.keys(tasks_pending_pattern)
		for tasks_pending_set_key in tasks_pending_set_keys:
		
			job_key = 'job-' + tasks_pending_set_key.decode()[14:]
			
			tasks = r.smembers(tasks_pending_set_key)
			tasks = list(tasks)
			for task_key in tasks:
				task_key = task_key.decode()
				
				item = {}
				item['job_id'] = job_key.split("-")[-1]
				item['description'] = r.hget(job_key, 'description').decode()
				
				item['port'] = r.hget(task_key, 'port').decode()
				
				
				addressing = r.hget(task_key, 'addressing').decode()
				if  addressing == "binary":
					item['data'] = 'BINARY'
				else:
					item['data'] = r.hget(task_key, 'data').decode()
				#endif
				
				item['job_access_key'] = encrypt(job_key)
				item['task_access_key'] = encrypt(task_key)
				task_latest.append(item)
			#endfor
		#endfor
		
		
		
		data  = {

					'job_latest': job_latest,
					'task_latest': task_latest,
				}
		

	return response(200, "ok", data)


def jobcounter(request):
	

	if request.method == 'GET':
		
		job_total_pattern = 'job-*'
		jobs = r.keys(job_total_pattern)
		job_total = len(jobs)
		
		
		job_pending = 0
		task_total = 0

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
			

		#endfor
		

		#task_pending
		work_pattern = 'work-*'
		work_pending_keys = r.keys(work_pattern)
		
		work_pending = 0
		for work_pending_key in work_pending_keys:
			work_pending = work_pending + r.llen(work_pending_key)
		#endfor
		
		

		
		data  = {
					'job_total': job_total,
					'task_total': task_total,
					'job_pending': job_pending,
					'work_pending': work_pending,
				}
		

	return response(200, "ok", data)


def inlist(request):
	

	if request.method == 'GET':
		
		job_total_pattern = 'job-*'
		jobs = r.keys(job_total_pattern)
		job_total = len(jobs)
		
		
		job_pending = 0
		task_total = 0
		
		jobs_list = []
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
			item = (create_time, length, job_id, description, encrypt(job_key))
			jobs_list.append(item)
			
		#endfor
		
		
		#job_latest sort by create_time
		jobs_list = sorted(jobs_list, key=lambda x: (x[0]))
		
		#work in list
		work_pattern = 'work-*'
		works = r.keys(work_pattern)
		
		works_list = []
		for task in works:
			job_key = 'job-' + task.decode()[5:-33]
			item = {}
			item['job_id'] = job_key.split("-")[-1]
			item['description'] =  r.hget(job_key, 'description').decode()
			
			item['port'] =  r.hget(task, 'port').decode()
			item['data'] =  r.hget(job_key, 'data').decode()
			
			works_list.append(item)
		#endfor
		
		
		
		data  = {
					'jobs_list': jobs_list,
					'works_list': works_list,
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



def peekjob(request):
	

	if request.method == 'GET':
		
		job_access_key = request.GET.get('job_access_key', 'nokey')
		
		if job_access_key == 'nokey':
			return response(403, "forbidden", [])
		#endif
		
		job_key = decrypt(job_access_key)

		if r.hget(job_key, 'state') is None:
			return response(404, "job not found", [])
		#endif
		
		data = {}
		
		data['job_id'] = job_key.split("-")[-1]
		
		data['state'] = r.hget(job_key, 'state').decode()

		data['create_time'] = r.hget(job_key, 'create_time').decode()
		data['finish_time'] = r.hget(job_key, 'finish_time').decode()
		
		data['vendor_id'] = r.hget(job_key, 'vendor_id').decode()
		data['worker_group'] = r.hget(job_key, 'worker_group').decode()

		
		data['meta'] = r.hget(job_key, 'meta').decode()
		data['description'] = r.hget(job_key, 'description').decode()
		data['priority'] = r.hget(job_key, 'priority').decode()
	
		data['length'] = r.hget(job_key, 'length').decode()
		


	return response(200, "ok", data)


def peektask(request):
	

	if request.method == 'GET':
		
		task_access_key = request.GET.get('task_access_key', 'nokey')
		if task_access_key == 'nokey':
			return response(403, "forbidden", [])
		#endif
		
		task_key = decrypt(task_access_key)

		if r.hget(task_key, 'state') is None:
			return response(404, "task not found", [])
		#endif
		
		data = {}
		
		data['state'] = r.hget(task_key, 'state').decode()
		data['note'] = r.hget(task_key, 'note').decode()
		#data['result'] = r.hget(task_key, 'result').decode()

		data['create_time'] = r.hget(task_key, 'create_time').decode()
		data['start_time'] = r.hget(task_key, 'start_time').decode()
		data['finish_time'] = r.hget(task_key, 'finish_time').decode()

		data['job_id'] = r.hget(task_key, 'job_id').decode()
		data['priority'] = r.hget(task_key, 'priority').decode()

		data['meta'] = r.hget(task_key, 'meta').decode()
		data['addressing'] = r.hget(task_key, 'addressing').decode()
		data['port'] = r.hget(task_key, 'port').decode()
		

	return response(200, "ok", data)



def peekfile(request):
	

	if request.method == 'GET':
		
		filename = request.GET.get('filename', '/nofile')

		

	return response(200, "ok", [])






