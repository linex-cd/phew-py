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
		
		for item in finished_tasks_list:
			logging.info('%d textise task(s) done' % finished_tasks_count)
			
			data = None
			try:
				
				job_id = item

				job_info = {}
				job_info['job_id'] = str(job_id)

				data = detail_job(session = session, job = job_info)

			except Exception:
				logging.exception('kafka_producer_thread get job detail occur.')
				traceback.print_exc()

			#endtry	
			
			if data is None:
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
						result = '{"bbox": [], "ocr": [], "hocr": [] }'
					#endif
					
					result = json.loads(result)
					
					bbox.append([result['bbox']])
					content.append([result['ocr']])
					hocr.append([result['hocr']])
					
					task_meta = json.loads(task['meta'])
					index.append(task_meta['index'])

				#endfor
				
				#重新按照index排序
				tmp = sorted(zip(index, bbox, content, hocr))
				index, bbox, content, hocr = zip(*tmp)
				
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
				result['candidates'] = []
				
				data = dict()
				data['task_id'] = job_meta['task_id']
				data['result'] = 'success'
				data['data'] = result
				data['bmsah'] = job_meta['bmsah']
				json_string = json.dumps(data, ensure_ascii=False)
				
				topic = job_meta['topic']
				
				logging.info("Kafka Sent message, topic is: {}, bmsah is: {}".format(topic, data['bmsah']))
				producer = KafkaProducer(bootstrap_servers=kafka_server, max_request_size=1024 * 1024 * 1024, compression_type='gzip')
			
				bytes_out = json_string.encode(encoding='utf8')
				data = zlib.compress(bytes_out)

				
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