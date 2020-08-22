import logging
import traceback

import os
import time

from kafka import KafkaConsumer
from kafka.vendor import six

from db import TaskRecord

import files

import config


kafka_server = config.kafka_server.split(',')


def main():
	logging.info("kafka_consumer_thread started")
	
	#等待历史任务完成
	
	while True:
		'''
		task_in_process_count = TaskRecord.task_count()
		if task_in_process_count == 0:
			#没有初始化和进行中的任务
			logging.info('No textise task in processing, now consumer is to read the next...')
		'''		
		try:
			#手动拉取任务消息
			message = None
			consumer = KafkaConsumer(config.consumer_topic, 
								bootstrap_servers = kafka_server, 
								enable_auto_commit = False, 
								session_timeout_ms = 100*1000, 
								request_timeout_ms = 110*1000, 
								max_poll_records = 1,
								group_id='ocr')
			
			while True:
				
				task = None
				message = consumer.poll();
				if len(message.keys()) > 0:
					for tp, records in six.iteritems(message):
						for record in records:
						
							logging.info('Received textise request')
							
							task = record
							data = task.value.decode('utf-8')
							
							#load from file
							if len(data) < 200:
								data = files.readfile('/kafkacache/'+data)
							#endif
							
							dic = TaskRecord.save_task(data)

							logging.info('Saved textise task: %s' % dic['bmsah'])
							
						#endfor
						
					#endfor
					consumer.commit()
					consumer.close()
					
					#等待任务完成后重连拉取任务
					break
				#endif
				
				#阻塞等待
				time.sleep(5);
			#endwhile
			
		except Exception:
			logging.exception('textise exception occur.')
			traceback.print_exc()
			#不能用sys.exit(-1)，否则只能退出线程，无法结束进程让容器重启
			os._exit(-1)
		
		#endtry
		
		'''		
		else:	
			logging.info('%d existed textise task(s) in processing, consumer is waiting for 30 seconds' % task_in_process_count)
			time.sleep(30)
		#endif
		'''
		
		time.sleep(10)
	#endwhile
	
#enddef


if __name__ == '__main__':
	main();	
#endif