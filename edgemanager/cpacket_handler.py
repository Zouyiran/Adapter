# -*- coding:utf-8 -*-
'''
Created on 2013年11月18日

@author: Zouyiran
'''

import struct
from config.config import *
from ctmb import *
global logger

class CPacketHandler(object):
    def __init__(self, packet, ip, segIP):
        self.packet = packet
        self.ip = ip
        self.segIP = segIP
         
    def run(self):   
        mbapHeader = self.packet[0:10]
        data = self.packet[10:]
        protocol = mbapHeader[2:4]
        protocol = struct.unpack("!H", protocol)[0]
        logger.info("接收到边缘网关（IP:%s）数据包" % self.ip)
        if protocol == 0x00:
            handler = CCTMBHandler(mbapHeader, data, self.ip, self.segIP)
            handler.run()

        else:
            logger.info("接收到数据为非CTMB协议数据，暂不支持")
