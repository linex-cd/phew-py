
import threading
from task import task_thread
from ping import ping_thread

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