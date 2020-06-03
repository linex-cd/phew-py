# api for monitor

from .init import *

def index(request):
	return redirect("/index.html")

def sysstate(request):
	

	if request.method == 'GET':
		
		data  = {
					'load': 76,
					'cpu': 63,
					'memory': 49,
					'gpu': 91,
					'disk': 34,
					'network': 73,
					'temp': 89,
				}
		

	return response(200, "ok", data)

def totalcounter(request):
	

	if request.method == 'GET':
		
		data  = {
					'tasks': 13234,
					'files': 34253,
					'inqueuetasks': 224242,
					'inqueuefiles': 555354,
				}
		

	return response(200, "ok", data)



def successcounter(request):
	

	if request.method == 'GET':
		
		data  = {
					'successtasks': 1234,
					'failedtasks': 3453,
					'successfiles': 22242,
					'failedfiles': 55554,
				}
		

	return response(200, "ok", data)


def vendorcounter(request):
	

	if request.method == 'GET':
		
		data  = {
					'vendors': 362,
					'cities': 17,
				}
		

	return response(200, "ok", data)





