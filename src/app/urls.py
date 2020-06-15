
from django.urls import path
from django.conf.urls.static import static

from . import state
from . import job
from . import task


urlpatterns = [
	path('', state.index),
	
	path('state/sysstate', state.sysstate),
	path('state/jobcounter', state.jobcounter),
	path('state/nodecounter', state.nodecounter),
	
	path('job/ping', job.ping),
	path('job/assign', job.assign),
	path('job/delete', job.delete),
	path('job/done', job.done),
	path('job/detail', job.detail),
	path('job/read', job.read),
	
	path('task/ping', task.ping),
	path('task/get', task.get),
	path('task/finish', task.finish),
	
]+ static("/", document_root="./www/")