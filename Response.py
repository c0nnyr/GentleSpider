# coding:utf-8
from BaseObject import BaseObject
from Header import Header
from Selector import Selector

class Response(BaseObject):

    def __init__(self, url, status=-1, header=None, body='', request=None):
        super(Response, self).__init__(auto_destroy=('header', 'selector'))
        self.header = Header(header or {})
        self.satus = int(status)
        self.request = request
        self._url = url
        self._body = body
        self.selector = Selector(self)

    @property
    def url(self):
        return self._url

    @property
    def body(self):
        return self._body

    @property
    def meta(self):
        return getattr(self.request, 'meta', {})

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)


