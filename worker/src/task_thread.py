import json;
import requests;
import time;

import config;

import traceback;


from porter import port_task;


from phewsdk.finish import finish_task
from phewsdk.get import get_task



def main():


	MAX_TRY_TIMES = 100
	CUR_TRY_TIMES = 0
	
	session = create_session()
	
	while True:
		time.sleep(1)
		
		#拉取任务
		task = None
		
		task = get_task(session)
		
		if task != None:
			
			if task == '':
				log('暂时没有任务')
				time.sleep(10)
				continue
				
			#endif
			
		else:
				
			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				return
			else:
				session = create_session()
				continue
		
			#endif
		#endif
		

		
		
		#根据任务类型分配port
		note = ''
		result = ''
		state = 'error'
		try:
			note, result = port_task(task)
			if result != None:
				state = 'done'
			else:
				result = ''
			#endif		
			
		except:
			log('操作任务失败')
			traceback.print_exc()

			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				return
			else:
				session = create_session()
				continue
			#endif
		#endtry
		
		
		#上传任务结果

		task['state'] = state
		task['note'] = note
		
		if type(result) == dict or type(result) == list or type(result) == tuple:
			result = json.dumps(result)
		#endif
		task['result'] = result

		ret = finish_task(session, task)
		

		if ret == True:
			#归零失败计数器
			CUR_TRY_TIMES = 0
		else:
			log('上传任务结果失败')
			traceback.print_exc()

			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				return
			else:
				session = create_session()
				continue
			#endif
		#endtry
		
		log('操作任务成功')
		
	#endwhile
#enddef

if __name__ == '__main__':
	pass
#endif