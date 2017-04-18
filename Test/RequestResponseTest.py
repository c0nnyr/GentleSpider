# coding:utf-8
from BaseSpider import BaseSpider
from SqlDBHelper import RequestResponseMap
from SqlDBHelper import session as db
import re, math, json, datetime
from Request import Request
from Response import Response
import GlobalMethod as M
import pprint

if __name__ == '__main__':
	for item in db.query(RequestResponseMap).all():
		item = Response.loads(item.response)
		if '/p3/' in item.url:
			pprint.pprint(item.__dict__)
			print item.body
