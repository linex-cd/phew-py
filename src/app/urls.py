
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static

from . import state
from . import job
from . import task


urlpatterns = [
	path('', state.index),
	
	path('state/sysstate', state.sysstate),
	path('state/jobcounter', state.jobcounter),
	path('state/nodecounter', state.nodecounter),
	path('state/latestwork', state.latestwork),
	path('state/inlist', state.inlist),
	path('state/errortasklist', state.errorlist),
	
	path('job/ping', job.ping),
	path('job/assign', job.assign),
	path('job/delete', job.delete),
	path('job/done', job.done),
	path('job/detail', job.detail),
	path('job/read', job.read),
	
	path('task/ping', task.ping),
	path('task/get', task.get),
	path('task/finish', task.finish),

	url(r'^state/peekjob/$', state.peekjob),
	url(r'^state/peektask/$', state.peektask),
	url(r'^state/peekfile/$', state.peekfile),
	
]+ static("/", document_root="./www/")