# coding:utf-8

from BaseHandler import BaseItemHandler
import SqlDBHelper

class SqlItemHandler(BaseItemHandler):

	def handle(self, item):
		if isinstance(item, (SqlDBHelper.RequestResponseMap, SqlDBHelper.ProxyItem)):
			from SqlDBHelper import session as db
		else:
			from Items import session as db
		db.merge(item)
		db.commit()
