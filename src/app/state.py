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

#-------------------------------------------------------------------------------
from app.config import data_dir 
from app.config import system_disk_dir 
from app.config import system_data_dir
from app.config import error_ttl

def sysstate(request):
	

	if request.method == 'GET':
		
		#REDIS DB  1G
		db = int(filesize(data_dir + 'redis.rdb') / (1024*1024*1024*1) * 100)

		
		#CPU
		cpu = int(psutil.cpu_percent())
		
		#memory
		memory =  int(psutil.virtual_memory().percent)
		
		#systemdisk
		systemdisk = int(psutil.disk_usage(system_disk_dir).percent)
		
		#datadisk
		datadisk = int(psutil.disk_usage(system_data_dir).percent)

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
		
		group = request.COOKIES['group']
		if group is None:
			group = ""
		#endif
		key = request.COOKIES['key']
		if key is None:
			key = ""
		#endif
		role = request.COOKIES['role']
		if role is None:
			role = ""
		#endif
		
		job_latest = []
		
		#job set of the worker role
		job_set = 'job_set-' + group + '-' + key + '-' + role
		#jobs = r.zrange(job_set, 0, -1)
		jobs = r.zrevrange(job_set, 0, -1)
		
		#remove expired keys
		time_now = int(time.time())
		time_ttl = time_now - int(error_ttl)
		r.zremrangebyscore(job_set, 0, time_ttl-1)
		
		for job in jobs:
		
			job_key = job.decode()
			
			item = {}
			
			#latest
			item['length'] = int(r.hget(job_key, 'length').decode())
			item['priority'] = int(r.hget(job_key, 'priority').decode())
			item['description'] = r.hget(job_key, 'description').decode()
			item['job_id'] = job_key.split("-")[-1]
			item['create_time'] = r.hget(job_key, 'create_time').decode()
			item['create_time_i'] = r.hget(job_key, 'create_time').decode()
			item['encrypt_job_key'] = encrypt(job_key)
		
			job_latest.append(item)
			
		#endfor
		
		#job_latest sort by create_time
		job_latest = sorted(job_latest, key=lambda x: (x['create_time']))
		job_latest = job_latest[-20:]

	
		#task_latest
		task_latest = []
		
		
		tasks_pending_set = 'tasks_pending_set-'  + group + '-' + key + '-' + role
		task_keys = list(r.smembers(tasks_pending_set))
		
		for task_key in task_keys:
			
			tmp = task_key.decode().split("-")
			
			job_key = 'job-' + tmp[1] + '-' + tmp[2] + '-' + tmp[3] + '-' + tmp[4]
			job_id =  tmp[4]
			
			task_key = task_key.decode()
			if  r.hget(job_key, 'description') == None:
				r.srem(tasks_pending_set, task_key)
				continue
			item = {}
			item['job_id'] = job_id

			item['description'] = r.hget(job_key, 'description').decode()
			
			start_time = r.hget(task_key, 'start_time')
			if start_time == None:
				#ignore deleted task
				continue
			#endif
			
			addressing = r.hget(task_key, 'addressing').decode()
			if  addressing == "binary":
				item['data'] = 'BINARY'
			else:
				item['data'] = r.hget(task_key, 'data').decode()
			#endif
			
			item['port'] = r.hget(task_key, 'port').decode()
			item['addressing'] = addressing
			item['create_time'] = int(r.hget(task_key, 'create_time').decode())
			
			item['job_access_key'] = encrypt(job_key)
			item['task_access_key'] = encrypt(task_key)
			task_latest.append(item)
			
		#endfor
		#task_latest sort by create_time
		task_latest = sorted(task_latest, key=lambda x: (x['create_time']))
		task_latest = task_latest[-20:]
		
		
		data  = {

					'job_latest': job_latest,
					'task_latest': task_latest,
				}
		

	return response(200, "ok", data)


def jobcounter(request):
	

	if request.method == 'GET':
	
		group = request.COOKIES['group']
		if group is None:
			group = ""
		#endif
		key = request.COOKIES['key']
		if key is None:
			key = ""
		#endif
		role = request.COOKIES['role']
		if role is None:
			role = ""
		#endif
		
		#job_total
		job_total = 0
		statistics_job_total_key = 'statistics_job_total-' + group + '-' + key + '-' + role
		job_total_0 = r.get(statistics_job_total_key)
		if job_total_0 is not None:
			job_total = int(job_total_0.decode())
		#endif
		
		#task_total
		task_total = 0
		statistics_task_total_key = 'statistics_task_total-' + group + '-' + key + '-' + role
		task_total_0 = r.get(statistics_task_total_key)
		if task_total_0 is not None:
			task_total = int(task_total_0.decode())
		#endif
		

		
		#job_pending
		job_pending = 0
		statistics_job_pending_key = 'statistics_job_pending-' + group + '-' + key + '-' + role
		
		job_pending_0 = r.get(statistics_job_pending_key)
		if job_pending_0 is not None:
			job_pending = int(job_pending_0.decode())
		#endif

		#work_pending
		work_pending = 0
		
		#get priority list
		priority_set = 'priority_set-' + group + '-' + key + '-' + role
		prioritys = r.zrevrange(priority_set, 0, -1)
		
		for priority in prioritys:
			work_key = 'work-' + group + '-' + key + '-' + role + '-' + priority.decode()
			work_pending = work_pending + r.llen(work_key)
		#enfor
		

		data  = {
					'job_total': job_total,
					'task_total': task_total,
					'job_pending': job_pending,
					'work_pending': work_pending,
				}
		

	return response(200, "ok", data)


#-------------------------------------------------------------------------------

def nodecounter(request):
	

	if request.method == 'GET':
		
		group = request.COOKIES['group']
		if group is None:
			group = ""
		#endif
		key = request.COOKIES['key']
		if key is None:
			key = ""
		#endif
		role = request.COOKIES['role']
		if role is None:
			role = ""
		#endif
		
		vendor_set = 'vendor_set-' + group + '-' + key + '-' + role
		vendor_keys = list(r.smembers(vendor_set))
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
		
		
		worker_set = 'worker_set-' + group + '-' + key + '-' + role
		worker_keys = list(r.smembers(worker_set))
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


#-------------------------------------------------------------------------------

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


from app.config import URI_dir 

def peekfile(request):
	

	if request.method == 'GET':
		
		filename = request.GET.get('filename', '/nofile')
		
		#只访问特定目录
		if filename.find(URI_dir) != 0 :
			return redirect("/index.html")
		#endif
		
		#禁止伪造目录
		if filename.find('/../') >=0 :
			return redirect("/index.html")
		#endif
		
		if existfile(filename) == False:
			return redirect("/index.html")
		#endif
		

		return responsefile(filename)
	
	return redirect("/index.html")


#-------------------------------------------------------------------------------

def percentage(request):
	

	if request.method == 'GET':
		
		group = request.COOKIES['group']
		if group is None:
			group = ""
		#endif
		key = request.COOKIES['key']
		if key is None:
			key = ""
		#endif
		role = request.COOKIES['role']
		if role is None:
			role = ""
		#endif
		

		addressing_data = {}
		
		#addressing_count
		statistics_task_addressing_set = 'statistics_task_addressing_set-' + group + '-' + key + '-' + role
		statistics_task_addressing_keys = list(r.smembers(statistics_task_addressing_set))
		
		for statistics_task_addressing_key in statistics_task_addressing_keys:
			statistics_task_addressing_key = statistics_task_addressing_key.decode()
			
			addressing = statistics_task_addressing_key.split("-")[-1]
			addressing_count = int(r.get(statistics_task_addressing_key).decode())
			
			if addressing not in addressing_data:
				addressing_data[addressing] = 0
			#endif
			addressing_data[addressing] = addressing_data[addressing] + addressing_count
			
		#endfor
		
		port_data = {}
		
		#port_count
		statistics_task_port_set = 'statistics_task_port_set-' + group + '-' + key + '-' + role
		statistics_task_port_keys = list(r.smembers(statistics_task_port_set))
		
		for statistics_task_port_key in statistics_task_port_keys:
			statistics_task_port_key = statistics_task_port_key.decode()
			
			port = statistics_task_port_key.split("-")[-1]
			port_count = int(r.get(statistics_task_port_key).decode())
			
			if port not in port_data:
				port_data[port] = 0
			#endif
			port_data[port] = port_data[port] + port_count
			
		#endfor
				
		data  = {
					'addressing': addressing_data,
					'port': port_data,
				}


	return response(200, "ok", data)

#-------------------------------------------------------------------------------

def errorlist(request):
	

	if request.method == 'GET':
		
		group = request.COOKIES['group']
		if group is None:
			group = ""
		#endif
		key = request.COOKIES['key']
		if key is None:
			key = ""
		#endif
		role = request.COOKIES['role']
		if role is None:
			role = ""
		#endif
		
		#--------------------
		task_total = 0
		error_jobs = []
		

		error_job_set_key = 'error_job-' + group + '-' + key + '-' + role
	
		time_now = int(time.time())
		time_ttl = time_now - int(error_ttl)
		jobs = list(r.zrangebyscore(error_job_set_key, time_ttl, time_now))
		
		#remove expired keys
		r.zremrangebyscore(error_job_set_key, 0, time_ttl-1)
		
		for job in jobs:
		
			job_key = job.decode()
			
			item = {}
			
			#latest
			item['length'] = int(r.hget(job_key, 'length').decode())
			item['priority'] = int(r.hget(job_key, 'priority').decode())
			item['description'] = r.hget(job_key, 'description').decode()
			item['job_id'] = job_key.split("-")[-1]
			item['create_time'] = r.hget(job_key, 'create_time').decode()
			item['create_time_i'] = r.hget(job_key, 'create_time').decode()
			item['encrypt_job_key'] = encrypt(job_key)
			
			
			error_jobs.append(item)
		
		#endfor
	
		
		
		#job_latest sort by create_time

		error_jobs = sorted(error_jobs, key=lambda x: (x[0]))
		
		
		#-------------------------------
		error_tasks = []
		
		
		error_task_set_key = 'error_task-' + group + '-' + key + '-' + role
		
		
		time_now = int(time.time())
		time_ttl = time_now - int(error_ttl)
		tasks = list(r.zrangebyscore(error_task_set_key, time_ttl, time_now))
		
		#remove expired keys
		r.zremrangebyscore(error_task_set_key, 0, time_ttl-1)
		
		for task in tasks:
			
			task_key = task.decode()
			
			item = {}
			
			tmp = task_key.split("-")
			worker_group = tmp[1]
			worker_key = tmp[2]
			worker_role = tmp[3]
			job_id = tmp[4]
			job_key = 'job-' +worker_group + '-' + worker_key + '-' + worker_role + '-' + job_id
			
			item['job_id'] = job_id
	
			if r.hget(job_key, 'description') is None:
				r.zrem(error_task_set_key, task_key)
				continue
			#endif
			item['description'] = r.hget(job_key, 'description').decode()
			
			start_time = r.hget(task_key, 'start_time')
			if start_time == None:
				#ignore deleted task
				
				continue
			#endif
			
			addressing = r.hget(task_key, 'addressing').decode()
			if  addressing == "binary":
				item['data'] = 'BINARY'
			else:
				item['data'] = r.hget(task_key, 'data').decode()
			#endif
			
			item['port'] = r.hget(task_key, 'port').decode()
			item['addressing'] = addressing
			item['create_time'] = int(r.hget(task_key, 'create_time').decode())
			
			item['job_access_key'] = encrypt(job_key)
			item['task_access_key'] = encrypt(task_key)
			
			error_tasks.append(item)
		#endfor
	
		
		
		#job_latest sort by create_time
		error_tasks = sorted(error_tasks, key=lambda x: (x["create_time"]))
		

		
		data  = {
					'error_jobs': error_jobs,
					'error_tasks': error_tasks,
				}
		

	return response(200, "ok", data)



