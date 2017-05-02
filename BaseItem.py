# coding:utf-8
class BaseItem(object):
	def __init__(self, **kwargs):
		super(BaseItem, self).__init__()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	def copy(self):
		pass

	def check_existence(self, session):
		return False
