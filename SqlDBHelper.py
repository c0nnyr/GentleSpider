# coding:utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime
import datetime, random, logging
import GlobalMethod as M
from Request import Request
from Response import Response

_engine, _session, _Model = M.create_db_engine('request_response_map')

class RequestResponseMap(_Model):
	__tablename__  = 'request_response_map'
	db = _session

	id = Column(Integer(),)
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
		return cls.db.query(cls).filter(cls.request == request_str).first()

	@classmethod
	def store(cls, request, response):
		request_response_pair = cls(request, response)
		cls.db.merge(request_response_pair)
		cls.db.commit()
		return request_response_pair.id

_Model.metadata.create_all(_engine)#类型建立后,才能这样建立表

_engine, _session, _Model = M.create_db_engine('proxy')

class ProxyItem(_Model):
	'''一条代理信息记录'''
	db = _session

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
	def get_proper_proxy(cls, http_type):
		try:
			usable_proxy_filter = and_(cls.http_type == http_type, cls.my_score > 0)
			usable_proxy_count = cls.db.query(cls).filter(usable_proxy_filter).count()
			if usable_proxy_count == 0:
				return None, None
			offset = random.randint(0, usable_proxy_count - 1)
			logging.info('use proxy of {} / {}'.format(offset, usable_proxy_count))
			proxy_item = cls.db.query(cls).filter(usable_proxy_filter).offset(offset).first()
			return {http_type.lower() : '{}:{}'.format(proxy_item.ip, proxy_item.port)}, proxy_item.my_score
		except Exception as ex:
			logging.info('Exception {} when using get_proxies'.format(ex))
			return None, None

	@classmethod
	def set_proxy_score(cls, proxy, score):
		for ip_port in proxy.itervalues():
			ip, port = ip_port.split(':')

			item = cls.db.query(cls).filter(and_(cls.ip == ip, cls.port == port)).first()
			item.my_score = score

			cls.db.merge(item)
			cls.db.commit()

	@classmethod
	def clear_all(cls):
		cls.db.query(cls).delete()

_Model.metadata.create_all(_engine)#类型建立后,才能这样建立表
