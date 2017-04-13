# coding:utf-8

from BaseHandler import BaseItemHandler
import SqlDBHelper as db

class SqlItemHandler(BaseItemHandler):

	def handle(self, item):
		db.session.merge(item)
		db.session.commit()
