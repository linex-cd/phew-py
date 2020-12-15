import os

#vendor for phew config
vendor_id = os.getenv('VENDOR_ID', '1')
vendor_name = os.getenv('VENDOR_NAME', 'Nanjing-Dev-vendor-node-1')
vendor_location = os.getenv('VENDOR_LOCATION', '南京')
only_for_priority = os.getenv('ONLY_FOR_PRIORITY', '0')

jobcenter_server = os.getenv('JOBCENTER_SERVER', '127.0.0.1:2020')

worker_group = os.getenv('WORKER_GROUP', 'Nanjing')
worker_key = os.getenv('WORKER_KEY', 'testkey12345')
worker_role = os.getenv('WORKER_ROLE', 'textise')



kafka_server = os.getenv('KAFKA_SERVER', '卡夫卡服务器')
db = os.getenv('DB', '存储结果的数据库')
instant_id = os.getenv('INSTANT_ID', '节点ID')


dockerdata_dir = '/data'

consumer_topic = 'ocr'
cv_result_topic = 'taskResult'
head_result_topic = 'headResult'
update_result_topic = 'updateResult'


#OSS
access_key_id = os.getenv('OSS_ACCESS_KEY_ID', '<你的AccessKeyId>')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET', '<你的AccessKeySecret>')
bucket_name = os.getenv('OSS_BUCKET', '<你的Bucket>')
endpoint = os.getenv('OSS_ENDPOINT', '<你的访问域名>')


