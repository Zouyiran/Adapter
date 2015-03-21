# -*- coding: utf-8 -*- 
'''
Created on 2013年10月16日

@author: Administrator
'''

from cserver import *
from config.globals import *
global logger

class EdgeManager(object):
    """1） 为边缘网关提供多线程服务，接收其发送的CTMB数据，支持多版本协议IPV4,IPV6，UDP4，UDP6；
       2） 为ControlManager模块提供内部服务，解析其传来的控制信息数据包并下发至边缘网关；
       3） port---边缘网关传输端口
         cmsg_port---与ControlManager内部交换数据端口
    """
    def __init__(self, port, cmsg_port):
        self.tcp4Server = CIPv4ServerTCP(port)
        self.udp4Server = CIPv4ServerUDP(port)
        self.tcp6Server = CIPv6ServerTCP(port)
        self.udp6Server = CIPv6ServerUDP(port)
        self.cmsgServer = CControlMSGServer(cmsg_port)
    
    def __del__(self):
        logger.info("服务器已经关闭")
        
    def run(self):
        globals.test = "2"
        threads = []          
        threads.append(self.tcp4Server)
        threads.append(self.udp4Server)
        threads.append(self.tcp6Server)
        threads.append(self.udp6Server)
        threads.append(self.cmsgServer)
                
        #各server里已有错误捕获  
        for thread in threads:           
            thread.start()
