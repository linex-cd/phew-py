import logging
import traceback
import zlib
import json
import os
import time
import requests


from kafka import  KafkaProducer
from kafka.vendor import six

from db import TaskRecord

from phewsdk.done import done_job
from phewsdk.detail import detail_job
from phewsdk.read import read_job
from phewsdk.delete import delete_job

import files

import config


kafka_server = config.kafka_server.split(',')

#--------------------------------------------------------------------------------------		
							

def main():
	logging.info("kafka_producer_thread started")
	
	#检查已经完成的任务列表
	while True:
		session = requests.session();
		
		finished_tasks_list = []
		try:
			rs = done_job(session = session)
			
			if rs is not None:
				finished_tasks_list = rs['done']
			#endif
		except Exception:
			logging.exception('kafka_producer_thread get done jobs occur.')
			traceback.print_exc()

		#endtry	
		
		finished_tasks_count = len(finished_tasks_list)
		if finished_tasks_count == 0:
			time.sleep(5)
			continue
		#endif
		
		logging.info('%d textise task(s) done' % finished_tasks_count)
		for item in finished_tasks_list:

			data = None

			job_id = item
			
			logging.info('done task job_id: %s' % job_id)

			job_info = {}
			job_info['job_id'] = str(job_id)

			data = detail_job(session = session, job = job_info)

			if data is None:
				logging.exception('kafka_producer_thread get job detail occur.')
				continue
			#endif
			
			try:
								
				id = job_id
				tasks = data['tasks']
				job_meta = json.loads(data['job']['meta'])
				
				bbox = []
				content = []
				hocr = []
				index = []
				for task in tasks:
					result = task['result']
					if result == '':
						result = '{"bbox": [[]], "ocr": [[]], "hocr": [[]] }'
					#endif
					
					result = json.loads(result)
					
					if 'bbox' not in result:
						result = {"bbox": [[]], "ocr": [[]], "hocr": [[]] }
					#endif
					
					
					bbox.append(result['bbox'])
					content.append(result['ocr'])
					hocr.append(result['hocr'])
					
					task_meta = json.loads(task['meta'])
					index.append(task_meta['index'])

				#endfor
				
				if len(index) > 0:
					#重新按照index排序
					tmp = sorted(zip(index, bbox, content, hocr))
					index, bbox, content, hocr = zip(*tmp)
				#endif
				
				#保存任务数据到数据库
				data = dict()
				data['bbox'] = bbox
				data['content'] = content
				data['hocr'] = hocr
				data['index'] = index
				result = json.dumps(data, ensure_ascii=False)
				TaskRecord.update_task(id = id, result = result, state='success')
			
				#发送卡夫卡消息

				result = dict()
				result['bbox'] = bbox
				result['content'] = content
				result['hocr'] = hocr
				result['index'] = index
				result['table_type'] = job_meta['is_tables']
				result['ignore'] = job_meta['ignore']
				result['candidates'] = []
				
				data = dict()
				data['task_id'] = job_meta['task_id']
				data['result'] = 'success'
				data['data'] = result
				data['bmsah'] = job_meta['bmsah']
				json_string = json.dumps(data, ensure_ascii=False)
				
				topic = job_meta['topic']
				
				logging.info("Kafka Sent message, job id is: {} topic is: {}, bmsah is: {}".format(job_id, topic, data['bmsah']))
				producer = KafkaProducer(bootstrap_servers=kafka_server, max_request_size=1024 * 1024 * 1024, compression_type='gzip')
			
				
				#load from file
				paths = []
				bmsahs = data['bmsah'].split('[')
				bmsah = bmsahs[0]
				type = ''
				if bmsah.find('检捕受')>=0:
					type = '0201'
				elif bmsah.find('刑捕受')>=0:
					type = '2031'
				elif bmsah.find('检起诉受')>=0:
					type = '0301'
				elif bmsah.find('刑诉受')>=0:
					type = '2001'
				elif bmsah.find('未起诉受')>=0:
					type = '1722'
				elif bmsah.find('未捕受')>=0:
					type = '1701'

				info = bmsahs[1]
				infos = info.split(']')
				# 年份
				year = infos[0]
				# 单位编码
				dwbm = infos[1][:6]

				paths.append(dwbm)
				paths.append(year)
				paths.append(type)
				paths.append(data['bmsah'])
				
				
				dirs = '/kafkacache/' + '/'.join(paths)
				if os.path.isdir(dirs) == False:
					os.makedirs(dirs);
				#endif
				
				filename = '/'.join(paths) + '/tmp_ocr-cv.json'
				files.writefile('/kafkacache/' + filename, json_string)
				data = filename.encode(encoding='utf8')
				
				#bytes_out = json_string.encode(encoding='utf8')
				#data = zlib.compress(bytes_out)
				
				producer.send(topic, data)
				producer.flush()
				
				#标记任务已读
				try:
				
					job_id = item

					job_info = {}
					job_info['job_id'] = str(job_id)

					read_job(session = session, job = job_info)

				
				except Exception:
					logging.exception('kafka_producer_thread mark job detail occur.')
					traceback.print_exc()

				#endtry
				
				#删除子任务数据
				try:
				
					job_id = item

					job_info = {}
					job_info['job_id'] = str(job_id)

					delete_job(session = session, job = job_info)

				
				except Exception:
					logging.exception('kafka_producer_thread delete job detail occur.')
					traceback.print_exc()

				#endtry	
				
			except Exception:
				logging.exception('textise exception occur.')
				traceback.print_exc()
				#不能用sys.exit(-1)，否则只能退出线程，无法结束进程让容器重启
				os._exit(-1)
			#endtry	

		#endfor
		time.sleep(10)
	#endwhile
#enddef


if __name__ == '__main__':
	main()
#endif