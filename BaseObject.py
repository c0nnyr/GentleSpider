# coding:utf-8

class BaseObject(object):

    def __init__(self, auto_destroy=()):
        super(BaseObject, self).__init__()
        self.auto_destroy = auto_destroy

    def destroy(self):
        for attr in self.auto_destroy:
            v = getattr(self, attr, None)
            if not v:
                continue
            if isinstance(v, BaseObject):
                v.destroy()
            elif isinstance(v, (list, tuple)):
                for _v in v:
                    if _v:
                        v.destroy()
            elif isinstance(v, dict):
                for _v in v.itervalues():
                    if _v:
                        v.destroy()

        self.__dict__.clear()
