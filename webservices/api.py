#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import PostInsCfgModify
from config.config import *
global logger

class index:
    def POST(self):
        try:
            method = web.input().method
            if method == "PostInsCfgModify":
                data = web.data()
                handler = PostInsCfgModify.Handler(data)
                response = handler.handle()
                return response
            else:
                return "未提供的方法"
        except Exception, e:
            logger.info(str(e))
            return "接口格式不正确"