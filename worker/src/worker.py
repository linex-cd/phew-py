
import threading
import time
import os

from task_thread import main as task_thread
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
	thread_list = list()
	thread_list.append(threading.Thread(target=task_thread, name='task_thread'))
	thread_list.append(threading.Thread(target=ping_thread, name='ping_thread'))

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

#enddef

if __name__ == '__main__':
	main()
#endif