# coding:utf-8

from BaseHandler import BaseItemHandler
import SqlDBHelper

class SqlItemHandler(BaseItemHandler):

	def handle(self, item):
		if isinstance(item, SqlDBHelper.RequestResponseMap):
			from SqlDBHelper import rr_session as db
		elif isinstance(item, SqlDBHelper.ProxyItem):
			from SqlDBHelper import p_session as db
		else:
			from Items import session as db
		db.merge(item)
		db.commit()
