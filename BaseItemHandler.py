# coding:utf-8

class BaseItemHandler(object):

	def handle(self, item):
		print item.__dict__
