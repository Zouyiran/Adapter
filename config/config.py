# -*- coding: utf-8 -*-
'''
Created on 2013年10月15日

@author: Administrator
'''

import os
import web
from log.cadapter_logger import CAdapterLogger

PROGRAM_ROOT = "/home/ch/adapter"
logger = CAdapterLogger()
segIP = {}
LOG_CONFIG_FILE = "logger.conf" 
#设备配置文件路径
XMLFILEPATH = PROGRAM_ROOT+ os.sep +  "configmanager" + os.sep + "SEG.xml"

#MongoDB配置
DATABASE_ADDR = "219.141.189.154"
DATABASE_PORT = 27017
DATABASE_USER = "" 
DATABASE_PASSWORD = ""
DATABASE_NAME = "sdc"

#内部通信配置
CMSG_ADDR = "127.0.0.1"
CMSG_PORT = 2222 #control_manager与edge_manager传送cmsg内部接口

#服务器网络配置
SERVER_PORT = 502
PROTO_ID = 0

#以下为web服务配置
templates = PROGRAM_ROOT + os.sep + "webservices" + os.sep + "templates"
render = web.template.render(templates, cache = False)

site_prefix = os.sep + "adapter"

urls = (
    site_prefix + os.sep + 'api', 'webservices.api.index'
)

app = web.application(urls, globals())

#管理平台地址及端口
MANAGE_ADDR = "219.141.189.154" 
MANAGE_PORT = 8087

#业务平台地址及端口
BUSINESS_ADDR = "219.141.189.154"
BUSINESS_PORT = 80
