# coding:utf-8
from BaseObject import BaseObject

class Header(BaseObject):

    def __init__(self, header_dct):
        super(Header, self).__init__()
        self.header_dct = {k.lower():v for k, v in header_dct.iteritems()}

    def __getitem__(self, item):
        item = item.lower()
        return self.header_dct[item]

    def get(self, item, default=None):
        item = item.lower()
        return self.header_dct.get(item, default)
