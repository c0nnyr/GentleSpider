# coding:utf-8

from BaseItemHandler import BaseItemHandler
import SqlDBHelper as db

class SqlHandler(BaseItemHandler):

	def handle(self, item):
		db.session.merge(item)
		db.session.commit()
