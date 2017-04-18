# coding:utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime
import datetime, random, logging
from Request import Request
from Response import Response

engine = create_engine('sqlite:///sys.sqlite')
session_marker = sessionmaker(bind=engine)
session = session_marker()
Model = declarative_base(name='Model')


class RequestResponseMap(Model):
	__tablename__  = 'request_response_map'

	id = Column(Integer(), primary_key=True, autoincrement=True)
	request = Column(Text(), primary_key=True)
	response = Column(Text())

	request_time = Column(DateTime())

	def __init__(self, request=None, response=None):
		super(RequestResponseMap, self).__init__()
		if request:
			self.request = request.dumps()
			self.id = self.gen_id()
		if response:
			self.response = response.dumps()

		self.request_time = datetime.datetime.now()

	_ID = 0
	@classmethod
	def gen_id(cls):
		cls._ID += 1
		return cls._ID

	@classmethod
	def get(cls, request):
		request_str = request.dumps()
		return session.query(cls).filter(cls.request == request_str).first()

class ProxyItem(Model):
	'''一条代理信息记录'''
	IS_ITEM = True

	__tablename__ = 'proxy'

	start_url = Column(Text())
	original_data = Column(Text())

	ip = Column(Text(), primary_key=True)
	port = Column(Integer(), primary_key=True)
	country = Column(Text())
	location = Column(Text())
	anonymouse_type = Column(Text())
	http_type = Column(Text())
	speed = Column(Integer())
	link_time = Column(Integer())
	living_time = Column(Float())
	validate_date = Column(DateTime())

	my_score = Column(Integer(), default=100)

	def __init__(self, **kwargs):
		super(ProxyItem, self).__init__()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	@classmethod
	def get_proxies(cls, url):
		if url.startswith('https'):
			http_type = 'HTTPS'
		elif url.startswith('http'):
			http_type = 'HTTP'
		else:
			return None
		try:
			usable_proxy_filter = and_(cls.http_type == http_type, cls.my_score != 0)
			usable_proxy_count = session.query(cls).filter(usable_proxy_filter).count()
			if usable_proxy_count == 0:
				return None
			offset = random.randint(0, usable_proxy_count - 1)
			proxy_item = session.query(cls).filter(usable_proxy_filter).offset(offset).first()
			return {http_type.lower() : '{}:{}'.format(proxy_item.ip, proxy_item.port)}
		except Exception as ex:
			logging.info('Exception {} when using get_proxies'.format(ex))
			return None

	@classmethod
	def score_proxies(cls, proxies, score):
		for ip_port in proxies.itervalues():
			ip, port = ip_port.split(':')
			port = int(port)

			item = session.query(cls).filter(and_(cls.ip == ip, cls.port == port)).first()
			item.my_score = score

			session.merge(item)
			session.commit()


Model.metadata.create_all(engine)#类型建立后,才能这样建立表
