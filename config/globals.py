# -*- coding: utf-8 -*-

class singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
#本类中定义所有全局变量
class globals(singleton):
    #设备状态表
    deviceMap = {}