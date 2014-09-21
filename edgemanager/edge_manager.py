# -*- coding: utf-8 -*- 
'''
Created on 2013年10月16日

@author: Administrator
'''

from cserver import *

global logger

class EdgeManager(object):
    """1） 为边缘网关提供多线程服务，接收其发送的CTMB数据，支持多版本协议IPV4,IPV6，UDP4，UDP6；
       2） 为ControlManager模块提供内部服务，解析其传来的控制信息数据包并下发至边缘网关；
       3） port---边缘网关传输端口
         cmsg_port---与ControlManager内部交换数据端口
    """
    def __init__(self,port,cmsg_port,target=None,args=None):
        self.tcp4Server=CIPv4ServerTCP(port,target,args)
        self.udp4Server=CIPv4ServerUDP(port,target,args)
        self.tcp6Server=CIPv6ServerTCP(port,target,args)
        self.udp6Server=CIPv6ServerUDP(port,target,args)
        self.cmsgServer=CControlMSGServer(cmsg_port,target,args)
    
    def __del__(self):
        logger.info("All servers are ending")
        
    def run(self):
        threads = []
        try:           
            threads.append(self.tcp4Server)
            threads.append(self.udp4Server)
            threads.append(self.tcp6Server)
            threads.append(self.udp6Server)
            threads.append(self.cmsgServer)
        except:
            print "initial  failed"
            logger.error("failed to start servers")
                  
        try: 
            for thread in threads:
                print "Ip server threads are starting"
                thread.start()
                print thread.getName()
                print "++++++++++++++++++++++++++++"
        except:
            print "start failed"
            logger.debug("failed to be start servers")
#——————————————————————————————————————————————————————————
def test():
    edgemanager=EdgeManager(502,2222)
    edgemanager.run()
    
if __name__ == "__main__":
    test()

