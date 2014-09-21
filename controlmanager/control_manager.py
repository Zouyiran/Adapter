# -*- coding: utf-8 -*-
'''
Created on 2013年11月18日

@author: Echo
'''
import socket,struct
from config.config import *

class ControlManager(object):
    """ControlManager 1) 接收业务平台传来的控制信息数据包，并解析
                      2）  将解析的控制数据包按一定格式发送到EdgeManager内部端口，由EdgeManager下发至边缘网关"""
    def __init__(self, host, port):
        self.host=host
        self.port=port
        
    def convertmac(self, mac):
        """ip 地址转化成整数"""

        mac = mac.split(".")
        bytestr = ""
        for byte in mac:
            byte = int(byte)
            byte = "%02x" % byte
            bytestr += byte

        bytestr = "0x" + bytestr
        return int(bytestr, 16)
    
    def CControlMSGClient(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((CMSG_ADDR, CMSG_PORT))
        
        cmsg_pdu = self.MakeCMSGPDU("241.0.0.1","0.0.1.0.241.0.0.1",0xFFFF,12)
        self.client.send(cmsg_pdu)
        self.client.close()
        
    def MakeCMSGPDU(self, segmac, scmac, register, data):
        """生成发送至EdgeManager的控制数据包，格式：边缘网关地址（4byte）+采控器地址（8byte）+寄存器地址（2byte）+控制数据（2byte）"""
        segmac=struct.pack("!I",self.convertmac(segmac))
        scmac=struct.pack("!Q",self.convertmac(scmac))
        register=struct.pack("<H",register)
        cdata=struct.pack("<H",data)
        
        pdu = segmac+scmac+register+cdata
        return pdu
    
if __name__ == "__main__":
    cManager = ControlManager("", 502)
    cManager.CControlMSGClient()
        