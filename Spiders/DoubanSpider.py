# coding:utf-8
from BaseSpider import BaseSpider
import GlobalMethod as M
from BaseItem import BaseItem
import pprint, urllib
from Request import Request, RequestImg
from BaseItem import BaseItem
from sqlalchemy import Column, Text, DateTime

_engine, _session, _Model = M.create_db_engine('book')
class BookItem(BaseItem, _Model):
	IS_ITEM = True
	__tablename__ = 'book'

	url = Column(Text(), primary_key=True)
	id = Column(Text())
	title = Column(Text())
	sub_title = Column(Text())
	pub = Column(Text())
	rating_nums = Column(Text())
	rating_count = Column(Text())
	description = Column(Text())
	book_price = Column(Text())
	img_url = Column(Text())

	def __init__(self, **kwargs):
		super(BookItem, self).__init__()
		for k, v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)

	def __str__(self):
		return '<BookItem>url {}, meta {}'.format(self.url, self._meta)

_Model.metadata.create_all(_engine)#类型建立后,才能这样建立表

class DoubanSpider(BaseSpider):

	BASE_URL = 'https://book.douban.com'

	start_urls = [
		'https://book.douban.com/tag/',
	]

	def parse(self, response):
		tag_urls = response.xpath('//table[@class="tagCol"]/tbody/tr/td/a/@href').extract()
		full_urls = [self.BASE_URL + urllib.quote(url.encode('utf-8')) for url in tag_urls]

		for tag_url, full_url in zip(tag_urls, full_urls):
			tag = tag_url[5:]#tag
			yield Request(full_url, callback='_parse_book_page', meta={'start_url':full_url, 'tag':tag})
			return

	def _parse_book_page(self, response):
		item_xpath = '//*[@id="subject_list"]/ul/li'
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='div[@class="info"]/h2/a/@href',),
			'id':dict(xpath='div[@class="info"]/h2/a/@href', re_filter=r'subject/(?P<extract>\S+?)/'),
			'title':dict(xpath='div[@class="info"]/h2/a/text()',),
			'sub_title':dict(xpath='div[@class="info"]/h2/a/span/text()',),
			'pub':dict(xpath='div[@class="info"]/div[@class="pub"]/text()',),
			'rating_nums':dict(xpath='div[@class="info"]/div/span[@class="rating_nums"]/text()',),
			'rating_count':dict(xpath='div[@class="info"]/div/span[@class="pl"]/text()',),
			'description':dict(xpath='div[@class="info"]/p/text()',),
			'book_price':dict(xpath='div[@class="info"]/div[@class="ft"]/div/span[@class="buy-info"]/a/text()',),
			'img_url':dict(xpath='div[@class="pic"]/a/img/@src',),
		}
		for item in self._parse_items_ex(response, item_xpath, attr_map, BookItem):
			yield item
			yield RequestImg(item.img_url)
