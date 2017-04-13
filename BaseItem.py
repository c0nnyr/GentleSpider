# coding:utf-8
class BaseItem(object):
	IS_ITEM = True
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)
