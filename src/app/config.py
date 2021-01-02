import os

#phew config
redis_host = os.getenv('PHEW_REDIS_HOST', '127.0.0.1')
data_dir = os.getenv('PHEW_DATA_DIR', '/jobcenterdata/')
system_disk_dir = os.getenv('PHEW_DISK_DIR', '/')
system_data_dir = os.getenv('PHEW_DATA_DIR', '/jobcenterdata/')
URI_dir = os.getenv('PHEW_URI_DIR', '/juanzong/')
error_ttl = os.getenv('PHEW_ERROR_TTL', '259200') #3600*24*3 , 3天

from platform import system as platform_system
sysstr = platform_system()

if sysstr == "Windows" :
	data_dir = os.getenv('PHEW_DATA_DIR', '../jobcenterdata/')
	system_disk_dir = os.getenv('PHEW_DISK_DIR', 'C:/')
	system_data_dir = os.getenv('PHEW_DATA_DIR', 'C:/')
	URI_dir = os.getenv('PHEW_URI_DIR', '../data/')