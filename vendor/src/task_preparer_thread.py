import logging
import traceback

import json
import os
import time
import requests
import oss2

import files
from db import TaskRecord

from phewsdk.assign import assign_job

import config




def prepare_task(task):

	from_instant_id = task['from_instant_id']
	id = task['id']
	task_id = task['task_id']
	images = json.loads(task['images'])
	bmsah = task['bmsah']
	is_tables = json.loads(task['is_tables'])
	is_head = is_tables[0] if len(is_tables) > 0 else ''
	saved_path = task['saved_path']

	topic = None
	if str(from_instant_id).startswith('cv_node'):
		topic = config.cv_result_topic
	elif str(from_instant_id).startswith('head_node'):
		topic = config.head_result_topic
	elif str(from_instant_id).startswith('update_node'):
		topic = config.update_result_topic
	else:
		topic = ''
	#endif

	
	job_id = id
	description = bmsah
	priority = 5

	job_info = {}
	job_info['job_id'] = str(job_id)
	job_info['description'] = description
	job_info['priority'] = priority
	
	meta = {}
	meta['task_id'] = task_id
	meta['bmsah'] = bmsah
	meta['is_tables'] = is_tables
	meta['is_head'] = is_head
	meta['topic'] = topic
	meta['saved_path'] = topic
	
	job_info['meta'] = json.dumps(meta)
	
	tasks = []

	count = len(images)
	for index in range(count):
		filename = images[index]
		
		#check if local file exists, if not then download from oss
		local_file = '/juanzong/'+filename
		
		if files.existfile(local_file):
			logging.info("using local file:"+filename)
			
		else:
			#mkdirs for download
			files.makedirsforfile(local_file)
			
			#download from aliyun oss
			filename = 'dzws/'+filename
		
			logging.info("downloading file:"+filename)
			try:
				
				bucket = oss2.Bucket(oss2.Auth(config.access_key_id, config.access_key_secret), config.endpoint, config.bucket_name)
				bucket.get_object_to_file(filename, local_file)

			except Exception as e:

				logging.info('download from oss exception occur.')
				traceback.print_exc()
			
			#endtry
		#endif

		#assign task
		
		port = 'test'
		if local_file.lower().find(".png") >= 0 or local_file.lower().find(".jpg") >= 0:
			
			port = 'ocr'

			if is_tables[index] != '':
				port = 'tableocr'
			#endif
		#endif

		if local_file.lower().find(".pdf") >= 0:
			port = 'pdf'
		#endif
		
		
		
		task = {}
		task['job_id'] = job_id
		task['addressing'] = 'URI'
		task['meta'] = '{"index": '+str(index)+'}'
		
		task['data'] = local_file
		
		task['port'] = port

		tasks.append(task)
	#endfor
	
	#assign job
	
	try:

		session = requests.session();
		rs = assign_job(session = session, job = job_info, tasks = tasks)
		
		if rs == True :
			TaskRecord.update_task(id = id, result = '', state = 'assigned')
		else:
			logging.exception('prepare_task assign_job error: %d: %s' % (rs['code'], rs['msg']))
		#endif
			
	except:

		logging.exception('prepare_task assign_job exception occur.')
		traceback.print_exc()
		
		
		time.sleep(30)
	#endtry

#enddef


def main():
	logging.info("task_preparer_thread started")
	
	MAX_TRY_TIMES = 100
	CUR_TRY_TIMES = 0
	while True:
		try:

			tasks = TaskRecord.find_init_tasks()
			
			for task in tasks:
				prepare_task(task)
			#endfor
			#处理后等待新任务
			CUR_TRY_TIMES = 0
			
		except:

			logging.exception('task_thread find_new_tasks exception occur.')
			traceback.print_exc()
			
			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				logging.exception('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				#不能用sys.exit(-1)，否则只能退出线程，无法结束进程让容器重启
				os._exit(-1)
			#endif

			logging.exception('find_new_tasks will retry in 30 seconds.')
			time.sleep(30)
		#endtry
		time.sleep(10)
	#endwhile

	
#enddef



if __name__ == '__main__':
	main()
#endif