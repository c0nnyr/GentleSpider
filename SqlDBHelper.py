# coding:utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime, LargeBinary
import datetime, random, logging
import GlobalMethod as M
from Request import Request
from Response import Response

#session.execute('VACUUM')#删除后用这个可以减小文件大小

class RequestResponseMap(declarative_base(name='request_response_map')):
	__tablename__  = 'request_response_map'

	id = Column(Integer(),)
	request = Column(LargeBinary(), primary_key=True)
	response = Column(LargeBinary())

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
	def get(cls, session, request):
		request_str = request.dumps()
		results = session.query(cls.response).filter(cls.request == request_str).first()
		if results:
			return Response.loads(results[0])
		return None

	@classmethod
	def store(cls, session, request, response):
		request_response_pair = cls(request, response)
		#session.merge(request_response_pair)
		#session.commit()
		return request_response_pair.id

class ProxyItem(declarative_base(name='proxy')):
	'''一条代理信息记录'''
	__tablename__ = 'proxy'

	_cur_url = Column(Text())
	_crawl_date = Column(Text())

	ip = Column(Text(), primary_key=True)
	port = Column(Text(), primary_key=True)
	country = Column(Text())
	location = Column(Text())
	anonymouse_type = Column(Text())
	http_type = Column(Text())
	speed = Column(Text())
	link_time = Column(Text())
	living_time = Column(Text())
	validate_date = Column(Text())

	DEFAULT_SCORE = 2
	my_score = Column(Integer(), default=DEFAULT_SCORE)


	def __init__(self, **kwargs):
		super(ProxyItem, self).__init__()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	@classmethod
	def get_proper_proxy(cls, session, http_type):
		try:
			usable_proxy_filter = and_(cls.http_type == http_type, cls.my_score > 0)
			usable_proxy_count = session.query(cls).filter(usable_proxy_filter).count()
			if usable_proxy_count == 0:
				return None, None
			offset = random.randint(0, usable_proxy_count - 1)
			logging.info('use proxy of {} / {}'.format(offset, usable_proxy_count))
			proxy_item = session.query(cls).filter(usable_proxy_filter).offset(offset).first()
			return {http_type.lower() : '{}:{}'.format(proxy_item.ip, proxy_item.port)}, proxy_item.my_score
		except Exception as ex:
			logging.info('Exception {} when using get_proxies'.format(ex))
			return None, None

	@classmethod
	def set_proxy_score(cls, session, proxy, score):
		for ip_port in proxy.itervalues():
			ip, port = ip_port.split(':')

			item = session.query(cls).filter(and_(cls.ip == ip, cls.port == port)).first()
			if item:
				item.my_score = score

				session.merge(item)
				session.commit()

	@classmethod
	def clear_all(cls, session):
		session.query(cls).delete()
		session.commit()
