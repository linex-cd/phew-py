
import threading
from task_thread import main as task_thread
from ping_thread import main as ping_thread

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