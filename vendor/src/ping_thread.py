import requests;
import time;


import traceback;

import config;
from phewsdk.ping import ping;


def main():


	MAX_TRY_TIMES = 100
	CUR_TRY_TIMES = 0
	
	session = requests.session()
	
	while True:
		time.sleep(30)
		try:
			#检测服务器
			result = ping(session)
			
			if result != None:
				#归零失败计数器
				CUR_TRY_TIMES = 0
				continue

			else:
				CUR_TRY_TIMES = CUR_TRY_TIMES + 1
				if CUR_TRY_TIMES>=MAX_TRY_TIMES:
					log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
					return
				else:
					session = requests.session()
					continue
				#endif
			#endif
			
			
	
		except:
			traceback.print_exc()
			
			CUR_TRY_TIMES = CUR_TRY_TIMES + 1
			if CUR_TRY_TIMES>=MAX_TRY_TIMES:
				log('MAX_TRY_TIMES %d reached, exit.' % MAX_TRY_TIMES)
				return
			else:
				session = requests.session()
				continue
			#endif

		#endtry
		
		
	#endwhile
#enddef


if __name__ == '__main__':
	pass;
#end
	
	
	
	