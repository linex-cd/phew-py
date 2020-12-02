#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def web_service_thread():
	params = ['web.py', 'runserver', '0.0.0.0:2020']
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
	try:
		from django.core.management import execute_from_command_line
		execute_from_command_line(params)
	except ImportError as exc:
		print('please install django')


if __name__ == '__main__':
	web_service_thread()
#end
