# coding:utf-8
#
#class BookItem(BaseItem, Model):
#	IS_ITEM = True
#	__tablename__ = 'book'
#
#	url = Column(Text(), primary_key=True)
#	id = Column(Text())
#	title = Column(Text())
#	sub_title = Column(Text())
#	pub = Column(Text())
#	rating_nums = Column(Text())
#	rating_count = Column(Text())
#	description = Column(Text())
#	book_price = Column(Text())
#	img_url = Column(Text())
#
#	def __init__(self, **kwargs):
#		super(BookItem, self).__init__()
#		for k, v in kwargs.iteritems():
#			if hasattr(self, k):
#				setattr(self, k, v)
#
#	def __str__(self):
#		return '<BookItem>url {}, meta {}'.format(self.url, self._meta)
#
#Model.metadata.create_all(engine)#类型建立后,才能这样建立表
