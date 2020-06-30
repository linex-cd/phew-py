
import logging

import threading
import time
import os

import config

from kafka_consumer_thread import main as kafka_consumer_thread
from kafka_producer_thread import main as kafka_producer_thread
from task_preparer_thread import main as task_preparer_thread
from ping_thread import main as ping_thread

def daemon_thread(thread_list):
	
	total_count = len(thread_list)
	while True:
		time.sleep(5)
		active_count = threading.active_count() - 2 #exclude main thread and daemon thread
		
		if active_count < total_count:
			print('daemon_thread: total %d, active now %d' % (total_count, active_count))
			print('good bye')
			os._exit(-1)
		#endif
	#endwhile
#enddef


def main():
	
	#log init
	log_dir = os.path.join(config.dockerdata_dir, 'log')
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	#endif
	
	logging.basicConfig(
		filename=os.path.join(log_dir, '{}.log'.format(config.instant_id)),
		level=logging.INFO,
		format='[%(levelname)s] %(asctime)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)
	
	#start threads
	thread_list = list()
	thread_list.append(threading.Thread(target=kafka_consumer_thread, name='kafka_consumer_thread'))
	thread_list.append(threading.Thread(target=kafka_producer_thread, name='kafka_producer_thread'))
	thread_list.append(threading.Thread(target=task_preparer_thread, name='task_preparer_thread'))
	thread_list.append(threading.Thread(target=ping_thread, name='ping_thread'))
	
	threading.Thread(target=daemon_thread, name='daemon_thread', args=(thread_list, )).start()
	
	for thread in thread_list:
		thread.start()
	#endfor
	
	for thread in thread_list:
		thread.join()
	#endfor
#enddef


if __name__ == '__main__':
	main()
#endif