
import threading
import time
import os

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


def task_thread():

	while True:
		print('task')
		time.sleep(2)
#enddef

def ping_thread():

	for i in range(10):
		print('ping_thread' +str(i))
		time.sleep(1)
		
#enddef


def main():
	thread_list = list()
	thread_list.append(threading.Thread(target=task_thread, name='task_thread'))
	thread_list.append(threading.Thread(target=ping_thread, name='ping_thread'))
	
	
	threading.Thread(target=daemon_thread, name='daemon_thread', args=(thread_list, )).start()
	
	for thread in thread_list:
		thread.start()

	for thread in thread_list:

		thread.join()
		
	

#enddef

if __name__ == '__main__':
	main()
#endif