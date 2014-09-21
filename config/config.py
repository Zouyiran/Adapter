# -*- coding: utf-8 -*-
'''
Created on 2013年10月15日

@author: Administrator
'''

from PyQt4 import QtCore
import os
from log.cadapter_logger import CAdapterLogger

logger = CAdapterLogger()
segIP = {}
LOG_CONFIG_FILE = "logger.conf" 
XMLFILEPATH = os.getcwd()+"\\configmanager\\SEG.xml"

DATABASE_USER = "adapter" 
DATABASE_PASSWORD = "123"
DATABASE_NAME = "datamanager"
COLLECTION_NAME = "DeviceInsHty"

CMSG_ADDR = "127.0.0.1"
CMSG_PORT = 2222 #control_manager与edge_manager传送cmsg内部接口

SERVER_PORT = 502
CLIENT_ADDR = "127.0.0.1"
CLIENT_PORT = 502
SEGMAC = "241.0.0.1"
SCMAC = "0.0.0.241.0.0.0.1"
PROTO_ID = 0

FREQ_ADDR = 0x00F5
TEMP_UPPER = 0x4100
TEMP_LOWER =  0x4101
MOISTURE_UPPER = 0x4102
MOISTURE_LOWER = 0x4103
EARTH_TEMP_UPPER = 0x4104
EARTH_TEMP_LOWER = 0x4105
EARTH_MOISTURE_UPPER = 0x4106
EARTH_MOISTURE_LOWER = 0x4107
CO2_UPPER = 0x4108
CO2_LOWER = 0x4109
ILLUM_UPPER = 0x410A
ILLUM_LOWER = 0x410B
COMMAND_ADDR = 0x2100

INI_FILE = "." + os.sep + "config.ini"

def loadConfig():
    global SERVER_PORT, CLIENT_ADDR, CLIENT_PORT
    settings = QtCore.QSettings(INI_FILE, QtCore.QSettings.IniFormat)
    SERVER_PORT = int(settings.value("server-port", SERVER_PORT).toString())
    CLIENT_ADDR = settings.value("client-addr", CLIENT_ADDR).toString()
    CLIENT_PORT = int(settings.value("client-port", CLIENT_PORT).toString())
