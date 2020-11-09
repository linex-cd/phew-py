#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import config


def web_service_thread():
	params = ['web.py', 'runserver', '0.0.0.0:'+config.server_port]
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		print('please install django')
		
	execute_from_command_line(params)


if __name__ == '__main__':

	web_service_thread()
