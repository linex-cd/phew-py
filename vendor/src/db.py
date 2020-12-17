
from datetime import datetime
import json
import config

import time


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime, Integer, desc, and_, or_, func



Base = declarative_base()
engine = create_engine(config.db, pool_recycle=3600, encoding="utf-8")

Base.metadata.create_all(engine)

#sess = sessionmaker(bind=engine)()

class TaskRecord(Base):
	__tablename__ = 'ocr_task_record'
	__table_args__ = {"useexisting": True}
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	task_id = Column(Integer, nullable=False)
	priority = Column(Integer, nullable=False)
	bmsah = Column(Text())
	images = Column(Text(), nullable=False)
	is_tables = Column(Text(), nullable=False)
	ignore = Column(Text(), nullable=False)
	length = Column(Integer, nullable=False)
	bbox_cache = Column(Text())
	result = Column(Text())
	saved_path = Column(Text())
	state = Column(String(16), default=0, nullable=False)
	instant_id = Column(String(32))
	from_instant_id = Column(String(16))
	create_time = Column(DateTime(), default=datetime.now)
	modify_time = Column(DateTime(), onupdate=datetime.now)


	@classmethod
	def update_task(self, id, result, state):
		
		sess = sessionmaker(bind=engine)()
		
		records = sess.query(TaskRecord).filter_by(id=id).all()
		for record in records:

			record.result = result
			record.state = state
			sess.add(record)
			sess.commit()
			
		#endfor
		
		sess.close()
		

	@classmethod
	def save_task(self, message):
		
		sess = sessionmaker(bind=engine)()
		
		data = json.loads(message)
		record = TaskRecord()
		record.task_id = data['task_id']
		record.priority = data['priority']  if 'priority' in data else 5
		record.bmsah = data['bmsah']
		record.images = json.dumps(data['images'], ensure_ascii=False)
		record.is_tables = json.dumps(data['is_tables'], ensure_ascii=False)
		record.ignore = json.dumps(data['ignore'], ensure_ascii=False)
		record.length = len(data['is_tables'])
		record.saved_path = data['savedPath'] if 'savedPath' in data else ''
		record.from_instant_id = data['instant_id']
		record.instant_id = config.instant_id
		record.result = None
		record.state = 'init'
		
		sess.add(record)
		sess.commit()
		sess.close()
		
		return data

	@classmethod
	def task_count(self):
		sess = sessionmaker(bind=engine)()
		record_count = sess.query(func.count(TaskRecord.id))\
						.filter(and_( or_(TaskRecord.state == 'init', TaskRecord.state == 'assigned'), TaskRecord.instant_id == config.instant_id))\
						.scalar()
		sess.close()
		
		return record_count;
	
	@classmethod
	def find_init_tasks(self, limitcount):
		
		sess = sessionmaker(bind=engine)()
		
		time.sleep(10);
		limitcount = 5
		
		query = sess.query(TaskRecord).filter(and_(TaskRecord.state=="init", TaskRecord.priority == config.only_for_priority )).limit(limitcount)
		
		if int(config.only_for_priority) == 0:
			query = sess.query(TaskRecord).filter(and_(TaskRecord.state=="init", TaskRecord.instant_id == config.instant_id)).order_by(desc('priority')).limit(limitcount)
			
		#endif
		time.sleep(10);
		records = query.all()
		sess.close()
		
		tasks = []
		for record in records:
			task = {}
			task['id'] = record.id
			task['task_id'] = record.task_id
			task['bmsah'] = record.bmsah
			task['images'] = record.images
			task['is_tables'] = record.is_tables
			task['ignore'] = record.ignore
			task['length'] = record.length
			task['saved_path'] = record.saved_path
			task['from_instant_id'] = record.from_instant_id
			task['priority'] = record.priority

			tasks.append(task)
		return tasks
		
	@classmethod
	def is_belong_instance_task(self, record_id):

		sess = sessionmaker(bind=engine)()
		records = sess.query(TaskRecord).filter(and_(TaskRecord.instant_id == config.instant_id, TaskRecord.id == record_id)).all()
		sess.close()
		
		if len(records) > 0 :
			return True
		
		return False
		
	
