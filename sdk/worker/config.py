import os

worker_id = os.getenv('WORKER_ID', '3')
worker_name = os.getenv('WORKER_NAME', 'Nanjing-Dev-worker-node-1')
worker_location = os.getenv('WORKER_LOCATION', '南京')

jobcenter_server = os.getenv('JOBCENTER_SERVER', '127.0.0.1:2020')
jobcenter_server = os.getenv('JOBCENTER_SERVER', '192.168.2.29:2020')

worker_group = os.getenv('WORKER_GROUP', 'Nanjing')
worker_key = os.getenv('WORKER_KEY', 'testkey12345')
worker_role = os.getenv('WORKER_ROLE', 'textise')




