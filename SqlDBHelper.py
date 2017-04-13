# coding:utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime
import datetime

engine = create_engine('sqlite:///data.sqlite')
session_marker = sessionmaker(bind=engine)
session = session_marker()
Model = declarative_base(name='Model')

class RequestResponseMap(Model):
	__tablename__  = 'request_response_map'

	id = Column(Integer(), autoincrement=True)
	request = Column(Text(), primary_key=True)
	response = Column(Text())

	request_time = Column(DateTime())

	def __init__(self, request=None, response=None):
		super(RequestResponseMap, self).__init__()
		if request:
			self.request = request.dumps()
		if response:
			self.response = response.dumps()

		self.request_time = datetime.datetime.now()

	@classmethod
	def get(cls, request):
		request_str = request.dumps()
		return session.query(cls).filter(cls.request == request_str).first()

Model.metadata.create_all(engine)#类型建立后,才能这样建立表
